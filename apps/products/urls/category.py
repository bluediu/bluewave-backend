# Libs
from django.urls import include, path

# Apps
import apps.products.apis.category as api

api_patterns = [
    path("list/", api.list_categories, name="list"),
    path("create/", api.create_category, name="create"),
    path(
        "<int:category_id>/",
        include(
            [
                path("get/", api.get_category, name="get"),
                path("update/", api.update_category, name="update"),
                path("products/", api.list_product_by_category, name="products"),
            ]
        ),
    ),
]
