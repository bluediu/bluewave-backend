# Libs
from django.urls import include, path

# Apps
import apps.products.apis.product as api

api_patterns = [
    path("list/", api.list_products, name="list"),
    path("list/latest/", api.list_latest_products, name="latest"),
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
