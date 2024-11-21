# Core
from functools import partial

# Libs
from django.forms import model_to_dict

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view, authentication_classes

from drf_spectacular.utils import OpenApiResponse, extend_schema

# Apps
from apps.users import forms as fr
from apps.users.services import user as sv

# Global
from common.functions import form_to_api_schema

_user_form_api_schema = partial(extend_schema, tags=["Forms"])


# **=========== Auth ===========**


# noinspection PyUnusedLocal
@_user_form_api_schema(
    summary="[Auth] login form",
    responses=OpenApiResponse(
        description="Auth form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_auth_form(request) -> Response:
    """Return an auth form schema."""
    form = form_to_api_schema(form=fr.AuthFormSchema)
    return Response(data=form, status=HTTP_200_OK)


# **=========== Users ===========**


# noinspection PyUnusedLocal
@_user_form_api_schema(
    summary="[User] create form",
    responses=OpenApiResponse(
        description="Create user form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_create_user_form(request) -> Response:
    """Return a user create form schema."""
    form = form_to_api_schema(form=fr.UserCreateForm)
    return Response(data=form, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_user_form_api_schema(
    summary="[User] update form",
    responses=OpenApiResponse(
        description="Update user form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_update_user_form(request, user_id: int) -> Response:
    """Return a user update form schema."""
    user_data = model_to_dict(sv.get_user(user_id))
    form_schema = form_to_api_schema(form=fr.UserUpdateForm(user_data=user_data))
    return Response(data=form_schema, status=HTTP_200_OK)
