from django.urls import include, path


# Apps urls
from apps.users.urls import urlpatterns as users_api
from apps.products.urls.product import api_patterns as product
from apps.products.urls.category import api_patterns as category
from apps.tables.urls.table import api_patterns as table
from apps.transactions.urls.order import api_patterns as order
from apps.transactions.urls.payment import api_patterns as payment

# Forms urls
from apps.users.urls.form import users_form_patterns as users_form
from apps.products.urls.form import products_form_patterns as products_form
from apps.tables.urls.form import tables_form_patterns as tables_form
from apps.transactions.urls.form import orders_form_patterns as orders_form

from apps.api.views import APISchemaView, APISpecsView


app_name = "api"

# <entity>_api = [path(".../", include((..., app_name), namespace=""))]
forms_api = [
    path("user/", include((users_form, app_name), namespace="user")),
    path("product/", include((products_form, app_name), namespace="product")),
    path("table/", include((tables_form, app_name), namespace="table")),
    path("order/", include((orders_form, app_name), namespace="order")),
]

products_api = [
    path("product/", include((product, app_name), namespace="product")),
    path("category/", include((category, app_name), namespace="category")),
]

tables_api = [
    path("table/", include((table, app_name), namespace="table")),
]

orders_api = [
    path("order/", include((order, app_name), namespace="order")),
]

payments_api = [
    path("payment/", include((payment, app_name), namespace="payment")),
]


urlpatterns = [
    path("schema/", APISchemaView.as_view(), name="schema"),
    path("specs/", APISpecsView.as_view(), name="specs"),
    path("users/", include((users_api, app_name), namespace="users")),
    path("products/", include((products_api, app_name), namespace="products")),
    path("tables/", include((tables_api, app_name), namespace="tables")),
    path("orders/", include((orders_api, app_name), namespace="orders")),
    path("payments/", include((payments_api, app_name), namespace="payments")),
    path(
        "forms/",
        include(
            (forms_api, app_name),
            namespace="forms",
        ),
    ),
]
