from django.urls import include, path

import apps.tables.apis.table as api

api_patterns = [
    path("list/", api.list_tables, name="list"),
    path("list/order_statuses/", api.list_table_order_statuses, name="order_statuses"),
    path("create/", api.create_table, name="create"),
    path("login/", api.login_table, name="login"),
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
