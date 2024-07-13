from django.urls import include, path

import apps.transactions.apis.order as api

api_patterns = [
    path("search/", api.search_orders, name="search"),
    path("register/", api.register_order, name="register"),
    path("register/bulk/", api.register_bulk_orders, name="register_bulk"),
    path(
        "<str:order_code>/",
        include(
            [
                path("update/", api.update_order, name="update"),
            ]
        ),
    ),
    path(
        "table/<str:table_code>/",
        include(
            [
                path("count/", api.get_order_count, name="count"),
                path("state/", api.get_order_state, name="state"),
                path("products/", api.list_order_products, name="list"),
                path("close_bulk/", api.close_orders, name="close"),
            ]
        ),
    ),
]
