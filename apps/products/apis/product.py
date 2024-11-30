# Core
from functools import partial
from typing import NotRequired, TypedDict

# Libs
from django.http import QueryDict

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter

# Apps
from apps.products.services import product as sv
from apps.products.serializers import product as srz
from apps.products.services.category import get_category

# Global
from common import functions as fn
from common.api import filter_parameter_spec
from common.decorators import permission_required


_product_api_schema = partial(extend_schema, tags=["Products"])

_product_id_params = OpenApiParameter(
    name="product_id",
    description="Product ID.",
    location=OpenApiParameter.PATH,
    type=int,
)


class _ProductSearchT(TypedDict):
    """An product search type."""

    filter_by: NotRequired[str]
    category: NotRequired[int]


def process_product_query_params(query_params: QueryDict) -> _ProductSearchT:
    """Return serialized and validated query parameters."""

    params: _ProductSearchT = {}

    filter_by = fn.validate_filter_query_param(query_params)
    params["filter_by"] = filter_by

    category = query_params.get("category")
    if category is not None:
        params["category"] = category

    return params


# noinspection PyUnusedLocal
@_product_api_schema(
    summary="Get product",
    parameters=[_product_id_params],
    request=srz.ProductCreateSerializer,
    responses=OpenApiResponse(
        response=srz.ProductInfoSerializer,
        description="Product successfully created.",
    ),
)
@api_view(["GET"])
@permission_required("products.view_product")
def get_product(request, product_id: int) -> Response:
    """Return a product's information."""

    product = sv.get_product(product_id)
    output = srz.ProductInfoSerializer(product)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_product_api_schema(
    summary="List products",
    parameters=[
        filter_parameter_spec(scope="products"),
        OpenApiParameter(
            "category",
            description="Category ID",
            type=int,
        ),
    ],
    responses=OpenApiResponse(
        response=srz.ProductInfoSerializer(many=True),
        description="Products successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("product.list_product")
def list_products(request) -> Response:
    """Return a list of products."""

    params = process_product_query_params(request.query_params)
    output = srz.ProductInfoSerializer(
        sv.list_products(**params),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_product_api_schema(
    summary="List latest products",
    responses=OpenApiResponse(
        response=srz.ProductLatestInfoSerializer(many=True),
        description="Products successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("product.list_product")
def list_latest_products(request) -> Response:
    """Return a list of five latest products."""

    output = srz.ProductLatestInfoSerializer(
        sv.list_latest_products(),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


@_product_api_schema(
    summary="Create product",
    request=srz.ProductCreateSerializer,
    responses=OpenApiResponse(
        response=srz.ProductInfoSerializer,
        description="Product successfully created.",
    ),
)
@api_view(["POST"])
@permission_required("product.create_product")
def create_product(request) -> Response:
    """Create a new product."""

    payload = srz.ProductCreateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    data["category"] = get_category(category_id=data["category"])
    product = sv.create_product(user=request.user, **data)
    output = srz.ProductInfoSerializer(product)
    return Response(data=output.data, status=HTTP_201_CREATED)


@_product_api_schema(
    summary="Update product",
    parameters=[_product_id_params],
    request=srz.ProductUpdateSerializer,
    responses=OpenApiResponse(
        response=srz.ProductInfoSerializer,
        description="Product successfully updated.",
    ),
)
@api_view(["PUT"])
@permission_required("product.change_product")
def update_product(request, product_id: int) -> Response:
    """Update a product."""

    payload = srz.ProductUpdateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    if data.get("category", None):
        data["category"] = get_category(category_id=data["category"])
    product = sv.update_product(
        product=sv.get_product(product_id),
        user=request.user,
        **data,
    )
    output = srz.ProductInfoSerializer(product)
    return Response(data=output.data, status=HTTP_200_OK)
