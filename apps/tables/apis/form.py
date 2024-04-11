from functools import partial

from django.forms import model_to_dict
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.tables import forms as fr
from apps.tables.services.table import get_table
from common.functions import form_to_api_schema


_table_form_api_schema = partial(extend_schema, tags=["Forms"])


# **=========== Category ===========**
# noinspection PyUnusedLocal
@_table_form_api_schema(
    summary="[Table] create form",
    responses=OpenApiResponse(
        description="Create table form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_create_table_form(request) -> Response:
    """Return a table create form schema."""
    form = form_to_api_schema(form=fr.TableCreateForm)
    return Response(data=form, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_table_form_api_schema(
    summary="[Table] update form",
    responses=OpenApiResponse(
        description="Update table form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_update_table_form(request, table_id: int) -> Response:
    """Return a table update form schema."""
    category_data = model_to_dict(get_table(table_id))
    form_schema = form_to_api_schema(form=fr.TableUpdateForm(category_data))
    return Response(data=form_schema, status=HTTP_200_OK)
