from django.urls import path

import apps.products.apis.form as api

products_form_patterns = [
    path("create_category/", api.get_create_category_form, name="create_category"),
    path(
        "<int:category_id>/update_category/",
        api.get_update_category_form,
        name="update_category",
    ),
]
