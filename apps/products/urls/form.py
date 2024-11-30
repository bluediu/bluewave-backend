# Libs
from django.urls import path

# Apps
import apps.products.apis.form as api

products_form_patterns = [
    path("create_category/", api.get_create_category_form, name="create_category"),
    path(
        "<int:category_id>/update_category/",
        api.get_update_category_form,
        name="update_category",
    ),
    path("filter/", api.get_filter_products_form, name="filter_products"),
    path("create_product/", api.get_create_product_form, name="create_product"),
    path(
        "<int:product_id>/update_product/",
        api.get_update_product_form,
        name="update_product",
    ),
]
