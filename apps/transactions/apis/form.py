from functools import partial

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.transactions import forms as fr
from common.functions import form_to_api_schema


_transaction_form_api_schema = partial(extend_schema, tags=["Forms"])


# noinspection PyUnusedLocal
@_transaction_form_api_schema(
    summary="[Order] register form",
    responses=OpenApiResponse(
        description="Register order form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_register_order_form(request, table_code: str) -> Response:
    """Return an order register form schema."""
    form_schema = form_to_api_schema(form=fr.OrderRegisterForm(table_code))
    return Response(data=form_schema, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_transaction_form_api_schema(
    summary="[Payment] register form",
    responses=OpenApiResponse(
        description="Register payment form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_register_payment_form(request) -> Response:
    """Return a payment register form schema."""
    form_schema = form_to_api_schema(form=fr.PaymentRegisterForm)
    return Response(data=form_schema, status=HTTP_200_OK)
