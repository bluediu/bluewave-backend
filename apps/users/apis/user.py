from functools import partial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

from common import functions as fn
from apps.users.services import user as sv
from common.api import filter_parameter_spec
from apps.users.serializers import user as srz
from common.decorators import permission_required
from common.api import id_response_spec, empty_response_spec


_user_api_schema = partial(extend_schema, tags=["Users"])
_user_id_params = OpenApiParameter(
    name="user_id",
    description="User ID.",
    location=OpenApiParameter.PATH,
    type=int,
)


# noinspection PyUnusedLocal
@_user_api_schema(
    summary="Get user",
    parameters=[_user_id_params],
    responses=OpenApiResponse(
        response=srz.UserInfoSerializer,
        description="User successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("users.view_user")
def get_user(request, user_id: int) -> Response:
    """Return a user's information."""
    user = sv.get_user(user_id)
    output = srz.UserInfoSerializer(user)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_user_api_schema(
    summary="List users",
    parameters=[filter_parameter_spec(scope="users")],
    responses=OpenApiResponse(
        response=srz.UserInfoSerializer(many=True),
        description="List of users successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("users.view_user")
def get_users(request) -> Response:
    """Return a list users."""
    filter_by = fn.validate_filter_query_param(request.query_params)
    output = srz.UserInfoSerializer(
        sv.get_users(
            user=request.user,
            filter_by=filter_by,
        ),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


@_user_api_schema(
    summary="Create user",
    request=srz.UserCreateSerializer,
    responses=id_response_spec("User", "User successfully created."),
)
@api_view(["POST"])
@permission_required("users.add_user")
def create_user(request) -> Response:
    """Create a new user"""
    payload = srz.UserCreateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    user = sv.create_user(request_user=request.user, **data)
    return Response(data={"user_id": user.id}, status=HTTP_201_CREATED)


@_user_api_schema(
    summary="Update user",
    parameters=[_user_id_params],
    request=srz.UserUpdateSerializer,
    responses=empty_response_spec("User successfully updated."),
)
@api_view(["PUT"])
@permission_required("users.change_user")
def update_user(request, user_id: int) -> Response:
    """Update a user."""
    payload = srz.UserUpdateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    user = sv.get_user(user_id)
    sv.update_user(user=user, request_user=request.user, **data)
    return Response(status=HTTP_200_OK)
