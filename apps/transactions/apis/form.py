# Core
from functools import partial

# Libs
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view, authentication_classes

from drf_spectacular.utils import OpenApiResponse, extend_schema

# Apps
from apps.transactions import forms as fr

# Global
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


# noinspection PyUnusedLocal
@_transaction_form_api_schema(
    summary="[Payment] search form",
    responses=OpenApiResponse(
        description="Search payment form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_search_payment_form(request) -> Response:
    """Return a payment search form schema."""

    form_schema = form_to_api_schema(form=fr.PaymentSearchForm())
    return Response(data=form_schema, status=HTTP_200_OK)
