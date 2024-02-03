from django.urls import include, path


from apps.users.urls import urlpatterns as users_api
from apps.products.urls.product import api_patterns as product
from apps.products.urls.category import api_patterns as category
from apps.users.urls.form import users_form_patterns as users_form

from apps.api.views import APISchemaView, APISpecsView


app_name = "api"

# <entity>_api = [path(".../", include((..., app_name), namespace=""))]
forms_api = [
    path("user/", include((users_form, app_name), namespace="user")),
]

products_api = [
    path("product/", include((product, app_name), namespace="product")),
    path("category/", include((category, app_name), namespace="category")),
]

urlpatterns = [
    path("schema/", APISchemaView.as_view(), name="schema"),
    path("specs/", APISpecsView.as_view(), name="specs"),
    path("users/", include((users_api, app_name), namespace="users")),
    path("products/", include((products_api, app_name), namespace="products")),
    path(
        "forms/",
        include(
            (forms_api, app_name),
            namespace="forms",
        ),
    ),
]

# -> localhost:5000/api/forms/user/login
