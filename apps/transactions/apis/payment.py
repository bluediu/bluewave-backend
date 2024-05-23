from functools import partial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.transactions.services import payment as sv
from apps.transactions.serializers import payment as srz
from apps.tables.services.table import get_table_by_code

from common.api import empty_response_spec
from common.decorators import permission_required

_payment_api_schema = partial(extend_schema, tags=["Payments"])


# noinspection PyUnusedLocal
@_payment_api_schema(
    summary="Get payment",
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
