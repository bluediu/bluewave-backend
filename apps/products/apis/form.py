from functools import partial

from django.forms import model_to_dict
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.products import forms as fr
from apps.products.services.category import get_category
from apps.products.services.product import get_product
from common.functions import form_to_api_schema


_product_form_api_schema = partial(extend_schema, tags=["Forms"])


# **=========== Category ===========**
@_product_form_api_schema(
    summary="[Category] create form",
    responses=OpenApiResponse(
        description="Create category form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_create_category_form(request) -> Response:
    """Return a category create form schema."""
    form = form_to_api_schema(form=fr.CategoryCreateForm)
    return Response(data=form, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_product_form_api_schema(
    summary="[Category] update form",
    responses=OpenApiResponse(
        description="Update category form successfully retrieved.",
    ),
)
@authentication_classes(None)
@api_view(["GET"])
def get_update_category_form(request, category_id: int) -> Response:
    """Return a category update form schema."""
    category_data = model_to_dict(get_category(category_id))
    form_schema = form_to_api_schema(form=fr.CategoryUpdateForm(category_data))
    return Response(data=form_schema, status=HTTP_200_OK)
