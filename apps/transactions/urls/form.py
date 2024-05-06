from django.urls import path

import apps.transactions.apis.form as api

orders_form_patterns = [
    path(
        "table/<str:table_code>/register/",
        api.get_register_order_form,
        name="register",
    ),
]
