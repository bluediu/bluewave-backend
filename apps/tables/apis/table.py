from functools import partial

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from drf_spectacular.utils import OpenApiResponse, extend_schema, OpenApiParameter

from apps.tables.services import table as sv
from apps.tables.serializers import table as srz
from common.decorators import permission_required
from common import functions as fn

_table_api_schema = partial(extend_schema, tags=["Tables"])

_table_id_params = OpenApiParameter(
    name="table_id",
    description="Table ID.",
    location=OpenApiParameter.PATH,
    type=int,
)


# noinspection PyUnusedLocal
@_table_api_schema(
    summary="Get table",
    parameters=[_table_id_params],
    responses=OpenApiResponse(
        response=srz.TableInfoSerializer,
        description="Table successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("tables.view_table")
def get_table(request, table_id: int) -> Response:
    """Return a table's information."""
    table = sv.get_table(table_id)
    output = srz.TableInfoSerializer(table)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_table_api_schema(
    summary="Login table",
    request=srz.TableLoginSerializer,
    responses=OpenApiResponse(
        response=srz.TableLoginTokenSerializer,
        description="Table login successfully.",
    ),
)
@authentication_classes(None)
@api_view(["POST"])
def login_table(request) -> Response:
    """Login table for clients app."""
    payload = srz.TableLoginSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    table = sv.login_table(table_code=data["code"])
    output = srz.TableLoginTokenSerializer(table)
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_table_api_schema(
    summary="List tables",
    responses=OpenApiResponse(
        response=srz.TableInfoSerializer(many=True),
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


# noinspection PyUnusedLocal
@_table_api_schema(
    summary="List table order statuses",
    responses=OpenApiResponse(
        response=srz.TableOrderStatusSerializer(many=True),
        description="Table order statuses successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("tables.list_table")
def list_table_order_statuses(request) -> Response:
    """Return a list of table order statuses."""
    output = srz.TableOrderStatusSerializer(
        sv.list_table_order_statuses(),
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
    table = sv.create_table(user=request.user, **data)
    output = srz.TableInfoSerializer(table)
    return Response(data=output.data, status=HTTP_201_CREATED)


@_table_api_schema(
    summary="Update table",
    parameters=[_table_id_params],
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
    output = srz.TableInfoSerializer(table)
    return Response(data=output.data, status=HTTP_200_OK)
