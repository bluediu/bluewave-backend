from functools import partial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter

from common import functions as fn
from common.api import filter_parameter_spec
from common.decorators import permission_required
from apps.products.services import category as sv
from apps.products.serializers import category as srz

_category_api_schema = partial(extend_schema, tags=["Categories"])

_category_id_params = OpenApiParameter(
    name="category_id",
    description="Category ID.",
    location=OpenApiParameter.PATH,
    type=int,
)


# noinspection PyUnusedLocal
@_category_api_schema(
    summary="Get category",
    parameters=[_category_id_params],
    request=srz.CategoryCreateSerializer,
    responses=OpenApiResponse(
        response=srz.CategoryInfoSerializer,
        description="Category successfully created.",
    ),
)
@api_view(["GET"])
@permission_required("products.view_category")
def get_category(request, category_id: int) -> Response:
    """Return a category's information."""
    category = sv.get_category(category_id)
    output = srz.CategoryInfoSerializer(category)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_category_api_schema(
    summary="List categories",
    parameters=[filter_parameter_spec(scope="categories"), _category_id_params],
    responses=OpenApiResponse(
        response=srz.CategoryInfoSerializer(many=True),
        description="Categories successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("products.list_category")
def list_categories(request) -> Response:
    """Return a list of categories."""
    filter_by = fn.validate_filter_query_param(request.query_params)
    output = srz.CategoryInfoSerializer(
        sv.list_categories(filter_by=filter_by),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_category_api_schema(
    summary="List products by category",
    parameters=[filter_parameter_spec(scope="products"), _category_id_params],
    responses=OpenApiResponse(
        response=srz.CategoryProductsInfoSerializer(many=True),
        description="Products by category successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("products.list_category")
def list_product_by_category(request, category_id: int) -> Response:
    """Return a list of products by category."""
    filter_by = fn.validate_filter_query_param(request.query_params)
    output = srz.CategoryProductsInfoSerializer(
        sv.get_products_by_category(category_id, filter_by),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


@_category_api_schema(
    summary="Create category",
    request=srz.CategoryCreateSerializer,
    responses=OpenApiResponse(
        response=srz.CategoryInfoSerializer,
        description="Category successfully created.",
    ),
)
@api_view(["POST"])
@permission_required("products.create_category")
def create_category(request) -> Response:
    """Create a new category."""
    payload = srz.CategoryCreateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    category = sv.create_category(user=request.user, **data)
    output = srz.CategoryInfoSerializer(category)
    return Response(data=output.data, status=HTTP_201_CREATED)


@_category_api_schema(
    summary="Update category",
    parameters=[_category_id_params],
    request=srz.CategoryUpdateSerializer,
    responses=OpenApiResponse(
        response=srz.CategoryInfoSerializer,
        description="Category successfully updated.",
    ),
)
@api_view(["PUT"])
@permission_required("products.change_category")
def update_category(request, category_id: int) -> Response:
    """Update a category."""
    payload = srz.CategoryUpdateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    category = sv.update_category(
        category=sv.get_category(category_id),
        user=request.user,
        **data,
    )
    output = srz.CategoryInfoSerializer(category)
    return Response(data=output.data, status=HTTP_200_OK)
