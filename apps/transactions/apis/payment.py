from functools import partial
from typing import NotRequired, TypedDict

from django.http import QueryDict
from django.utils.timezone import now
from django.core.validators import ValidationError

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, extend_schema

from apps.transactions.services import payment as sv
from apps.transactions.serializers import payment as srz
from apps.tables.services.table import get_table_by_code
from apps.transactions.models.payment import PaymentType

from common import functions as fn
from common.api import empty_response_spec
from common.decorators import permission_required

_payment_api_schema = partial(extend_schema, tags=["Payments"])

_payment_code_params = OpenApiParameter(
    name="code",
    description="Payment code.",
    location=OpenApiParameter.PATH,
)

_table_code_params = OpenApiParameter(
    name="table_code",
    description="Table code.",
    location=OpenApiParameter.PATH,
)


payment_search_params_specs = [
    OpenApiParameter(
        "type",
        description=f"Payment type",
        enum=[item for item in PaymentType],
    ),
    OpenApiParameter("code", description="Table code"),
    OpenApiParameter("since", description="Payment since date"),
    OpenApiParameter("until", description="Payment until date"),
]


class _PaymentSearchT(TypedDict):
    """An order search type."""

    code: NotRequired[int]
    payment_type: str
    since: NotRequired[str]
    until: NotRequired[str]


def process_payment_query_params(query_params: QueryDict) -> _PaymentSearchT:
    """Return serialized and validated order query parameters."""
    params: _PaymentSearchT = {}

    code = query_params.get("code")
    if code is not None:
        params["code"] = code

    payment_type = query_params.get("payment_type")
    if payment_type is not None:
        values = PaymentType.values
        values.append("ALL")
        if payment_type not in values:
            raise ValidationError({"payment_type": "Invalid value."})
        params["payment_type"] = payment_type

    since = query_params.get("since")
    until = query_params.get("until")

    if since is not None:
        params["since"] = since

    if until is not None:
        params["until"] = until

    missing_field_message = "Both dates are required to search by date range."
    if until and not since:
        raise ValidationError({"since": missing_field_message})
    if since and not until:
        raise ValidationError({"until": missing_field_message})

    if since and until and fn.parse_date(since) > fn.parse_date(until):
        raise ValidationError({"until": "It can't be before the start."})

    if until and fn.parse_date(until) > now().date():
        raise ValidationError({"until": "Must be earlier or equal than today."})

    return params


# noinspection PyUnusedLocal
@_payment_api_schema(
    summary="List orders by payment",
    parameters=[_payment_code_params],
    responses=OpenApiResponse(
        response=srz.PaymentOrdersInfoSerializer(many=True),
        description="Payment orders successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("transaction.list_payment")
def list_orders_by_payments(request, code: str) -> Response:
    """Retrieve orders for a payment."""
    orders = sv.list_orders_by_payment(code)
    output = srz.PaymentOrdersInfoSerializer(orders, many=True)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_payment_api_schema(
    summary="Get payment",
    parameters=[_table_code_params],
    responses=OpenApiResponse(
        response=srz.PaymentInfoSerializer,
        description="Payment successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("transaction.view_payment")
def get_payment(request, table_code: str) -> Response:
    """
    Return a payment's information.

    It returns an empty response if no payment is found.
    """
    payment = sv.get_payment(table_code)
    output = None
    if payment:
        output = srz.PaymentInfoSerializer(payment).data
    return Response(data=output, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_payment_api_schema(
    summary="Payments history",
    parameters=payment_search_params_specs,
    responses=OpenApiResponse(
        response=srz.PaymentInfoSerializer(many=True),
        description="Payments successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("transactions.list_payment")
def list_payments_history(request) -> Response:
    """Retrieve a list of payments."""
    params = process_payment_query_params(request.query_params)
    payments = sv.search_payments(**params)
    output = srz.PaymentInfoSerializer(payments, many=True)
    return Response(data=output.data, status=HTTP_200_OK)


@_payment_api_schema(
    summary="Register payment",
    request=srz.PaymentRegisterSerializer,
    responses=empty_response_spec("Payment successfully registered."),
)
@api_view(["POST"])
@permission_required("transactions.create_payment")
def register_payment(request) -> Response:
    """Register a payment."""
    payload = srz.PaymentRegisterSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    data["table"] = get_table_by_code(table_code=data["table"])
    sv.register_payment(user=request.user, fields=data)
    return Response(status=HTTP_201_CREATED)


@_payment_api_schema(
    summary="Close a payment",
    parameters=[_table_code_params],
    request=None,
    responses=empty_response_spec("Payment successfully closed."),
)
@api_view(["PUT"])
@permission_required("transactions.change_payment")
def close_payment(request, table_code: str) -> Response:
    """
    Close a payment.

    This action involves changing the payment status to 'PAID' and setting
    the 'is_closed' status to True for all orders associated with this payment.
    """
    table = get_table_by_code(table_code=table_code)
    sv.close_payment(user=request.user, table=table)
    return Response(data={"ok": True}, status=HTTP_200_OK)
