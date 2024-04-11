from functools import partial

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.tables.services import table as sv
from apps.tables.serializers import table as srz
from common.decorators import permission_required
from common import functions as fn

_table_api_schema = partial(extend_schema, tags=["Tables"])


# noinspection PyUnusedLocal
@_table_api_schema(
    summary="Get table",
    request=srz.TableCreateSerializer,
    responses=OpenApiResponse(
        response=srz.TableInfoSerializer,
        description="Table successfully created.",
    ),
)
@api_view(["GET"])
@permission_required("tables.view_table")
def get_table(request, table_id: int) -> Response:
    """Return a table's information."""
    category = sv.get_table(table_id)
    output = srz.TableInfoSerializer(category)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_table_api_schema(
    summary="List tables",
    responses=OpenApiResponse(
        response=srz.TableCreateSerializer(many=True),
        description="Tables successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("tables.list_table")
def list_tables(request) -> Response:
    """Return a list of tables."""
    filter_by = fn.validate_filter_query_param(request.query_params)
    output = srz.TableInfoSerializer(
        sv.list_tables(filter_by=filter_by),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


@_table_api_schema(
    summary="Create table",
    request=srz.TableCreateSerializer,
    responses=OpenApiResponse(
        response=srz.TableInfoSerializer,
        description="Table successfully created.",
    ),
)
@api_view(["POST"])
@permission_required("tables.create_table")
def create_table(request) -> Response:
    """Create a new table."""
    payload = srz.TableCreateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    category = sv.create_table(user=request.user, **data)
    output = srz.TableInfoSerializer(category)
    return Response(data=output.data, status=HTTP_201_CREATED)


@_table_api_schema(
    summary="Update table",
    request=srz.TableUpdateSerializer,
    responses=OpenApiResponse(
        response=srz.TableInfoSerializer,
        description="Table successfully updated.",
    ),
)
@api_view(["PUT"])
@permission_required("tables.change_table")
def update_table(request, table_id: int) -> Response:
    """Update a table."""
    payload = srz.TableUpdateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    table = sv.update_table(
        table=sv.get_table(table_id),
        user=request.user,
        **data,
    )
    output = srz.TableUpdateSerializer(table)
    return Response(data=output.data, status=HTTP_200_OK)