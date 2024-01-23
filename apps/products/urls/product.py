from django.urls import include, path

import apps.products.apis.product as api

api_patterns = [
    path("list/", api.list_products, name="list"),
    path("create/", api.create_product, name="create"),
    path(
        "<int:product_id>/",
        include(
            [
                path("get/", api.get_product, name="get"),
                path("update/", api.update_product, name="update"),
            ]
        ),
    ),
]
