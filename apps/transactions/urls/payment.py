# Libs
from django.urls import include, path

# Apps
import apps.transactions.apis.payment as api

api_patterns = [
    path("list/", api.list_payments_history, name="list"),
    path("register/", api.register_payment, name="register"),
    path(
        "<str:code>/",
        include(
            [
                path("orders/", api.list_orders_by_payments, name="list_orders"),
            ]
        ),
    ),
    path(
        "table/<str:table_code>/",
        include(
            [
                path("get/", api.get_payment, name="get"),
                path("close/", api.close_payment, name="close"),
            ]
        ),
    ),
]
