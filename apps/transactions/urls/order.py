from django.urls import include, path

import apps.transactions.apis.order as api

api_patterns = [
    path("search/", api.search_orders, name="search"),
    path("register/", api.register_order, name="register"),
    path(
        "table/<str:table_code>/products/",
        api.list_order_products,
        name="list",
    ),
]
