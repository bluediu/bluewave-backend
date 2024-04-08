from django.urls import include, path

import apps.tables.apis.table as api

api_patterns = [
    path("list/", api.list_tables, name="list"),
    path("create/", api.create_table, name="create"),
    path(
        "<int:table_id>/",
        include(
            [
                path("get/", api.get_table, name="get"),
                path("update/", api.update_table, name="update"),
            ]
        ),
    ),
]
