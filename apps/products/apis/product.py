from functools import partial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.products.services import product as sv
from apps.products.serializers import product as srz
from apps.products.services.category import get_category
from common.decorators import permission_required

_product_api_schema = partial(extend_schema, tags=["Products"])


@_product_api_schema(
    summary="Get product",
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
    responses=OpenApiResponse(
        response=srz.ProductInfoSerializer(many=True),
        description="Products successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("product.list_product")
def list_products(request) -> Response:
    """Return a list of products."""
    output = srz.ProductInfoSerializer(sv.list_products(), many=True)
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
