from functools import partial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.users import forms as fr
from common.functions import form_to_api_schema

_user_form_api_schema = partial(extend_schema, tags=["Forms"])


# noinspection PyUnusedLocal
@_user_form_api_schema(
    summary="Auth form",
    responses=OpenApiResponse(
        description="Auth form successfully retrieved.",
    ),
)
@api_view(["GET"])
def get_auth_form(request) -> Response:
    """Return an auth form schema."""
    form = form_to_api_schema(form=fr.AuthFormSchema)
    return Response(data=form, status=HTTP_200_OK)
