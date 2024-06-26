from functools import partial
from typing import NotRequired, TypedDict

from django.http import QueryDict
from django.core.validators import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, extend_schema

from apps.transactions.models import OrderStatus
from apps.transactions.services import order as sv
from apps.transactions.serializers import order as srz
from apps.tables.services.table import get_table_by_code
from apps.products.services.product import get_product

from common.api import empty_response_spec
from common.decorators import permission_required

_order_api_schema = partial(extend_schema, tags=["Orders"])

order_search_params_specs = [
    OpenApiParameter("table_id", description="Table ID", type=int),
    OpenApiParameter(
        "status",
        description=f"Order status",
        enum=[item for item in OrderStatus],
    ),
    OpenApiParameter("close", description="Order close", type=bool),
]


class _OrderSearchT(TypedDict):
    """An order search type."""

    table_id: NotRequired[int]
    status: NotRequired[str]
    close: NotRequired[bool]


def process_order_query_params(query_params: QueryDict) -> _OrderSearchT:
    """Return serialized and validated order query parameters."""
    params: _OrderSearchT = {}
    params_count = 0

    table_id = query_params.get("table_id")
    if table_id is not None:
        try:
            params["table_id"] = int(table_id)
            params_count += 1
        except ValueError:
            raise ValidationError({"table_id": "Invalid value."})

    status = query_params.get("status")
    if status is not None:
        if status not in OrderStatus.values:
            raise ValidationError({"status": "Invalid value."})
        params["status"] = status
        params_count += 1

    close = query_params.get("close")
    if close is not None:
        params["close"] = True if close == "true" else False
        params_count += 1

    return params


# noinspection PyUnusedLocal
@_order_api_schema(
    summary="Get order state",
    responses=OpenApiResponse(
        response=srz.OrderStateInfoSerializer,
        description="Order state successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("tables.get_order")
def get_order_state(request, table_code: str) -> Response:
    """Get order state information."""
    data = sv.get_order_state(table_code)
    output = srz.OrderStateInfoSerializer(data)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_order_api_schema(
    summary="Search orders",
    parameters=order_search_params_specs,
    responses=OpenApiResponse(
        response=srz.OrderInfoSerializer(many=True),
        description="Orders successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("tables.list_table")
def search_orders(request) -> Response:
    """Retrieve a table's orders."""
    params = process_order_query_params(request.query_params)
    orders = sv.search_orders(**params)
    output = srz.OrderInfoSerializer(orders, many=True)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_order_api_schema(
    summary="List products by table order",
    parameters=order_search_params_specs,
    responses=OpenApiResponse(
        response=srz.OrderProductsInfoSerializer(many=True),
        description="Order products successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("tables.list_table")
def list_order_products(request, table_code: str) -> Response:
    """Retrieve products for a table order."""
    orders = sv.list_order_products(table_code)
    output = srz.OrderProductsInfoSerializer(orders, many=True)
    return Response(data=output.data, status=HTTP_200_OK)


@_order_api_schema(
    summary="Register order",
    request=srz.OrderRegisterSerializer,
    responses=empty_response_spec("Order successfully registered."),
)
@api_view(["POST"])
@permission_required("transactions.create_order")
def register_order(request) -> Response:
    """Register a new order/transaction."""
    payload = srz.OrderRegisterSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    data["table"] = get_table_by_code(table_code=data["table"])
    data["product"] = get_product(product_id=data["product"])
    sv.register_order(user=request.user, fields=data)
    return Response(status=HTTP_201_CREATED)


@_order_api_schema(
    summary="Update order",
    request=srz.OrderUpdateSerializer,
    responses=empty_response_spec("Order successfully updated."),
)
@api_view(["PUT"])
@permission_required("transactions.change_order")
def update_order(request, order_code: str) -> Response:
    """
    Update an order.

    This endpoint allows updating the `quantity` of ordered products
    and the `status` of the order.

    **Constrains & consideration:**

    - **Canceled order:** The status of a canceled orders should remain unchanged.
    - **Canceled order & quantity:** If the order is canceled, it raises a validation
    error to prevent any further updates to the quantity,
    as canceled orders should remain unchanged.
    - **Delivered order:** Quantity updates are limited to prevent decreases.
        If the quantity is increased, the order status shifts to "Pending" to
        reflect additional products awaiting delivery.
    """
    payload = srz.OrderUpdateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    sv.update_order(
        order=sv.get_order(order_code),
        user=request.user,
        **data,
    )
    return Response(status=HTTP_200_OK)


@_order_api_schema(
    summary="Close all orders",
    request=None,
    responses=empty_response_spec("Orders successfully closed."),
)
@api_view(["PUT"])
@permission_required("transactions.change_order")
def close_orders(request, table_code: str) -> Response:
    """
    Close all orders.

    NOTE: This action is only available for tables that have all their orders
    `canceled` for some reason.
    """
    table = get_table_by_code(table_code=table_code)
    sv.close_orders_bulk(user=request.user, table=table)
    return Response(status=HTTP_200_OK)
