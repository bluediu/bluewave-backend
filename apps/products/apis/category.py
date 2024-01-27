from functools import partial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.products.serializers import category as srz
from apps.products.services import category as sv
from common.decorators import permission_required

_category_api_schema = partial(extend_schema, tags=["Categories"])


# noinspection PyUnusedLocal
@_category_api_schema(
    summary="Get category",
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
    responses=OpenApiResponse(
        response=srz.CategoryInfoSerializer(many=True),
        description="Categories successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("products.list_category")
def list_categories(request) -> Response:
    """Return a list of categories."""
    output = srz.CategoryInfoSerializer(sv.list_categories(), many=True)
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