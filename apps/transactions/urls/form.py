from django.urls import path

import apps.transactions.apis.form as api

orders_form_patterns = [
    path(
        "table/<str:table_code>/register/",
        api.get_register_order_form,
        name="register",
    ),
    path("register_payment/", api.get_register_payment_form, name="register_payment"),
    path("search_payments/", api.get_search_payment_form, name="search_payments"),
]
