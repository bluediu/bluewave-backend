from django.urls import include, path

import apps.transactions.apis.payment as api

api_patterns = [
    path("register/", api.register_payment, name="register"),
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
