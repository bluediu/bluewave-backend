from django.urls import include, path


from apps.users.urls import urlpatterns as user_api
from apps.api.views import APISchemaView, APISpecsView


app_name = "api"

# <entity>_api = [path(".../", include((..., app_name), namespace=""))]

urlpatterns = [
    path("schema/", APISchemaView.as_view(), name="schema"),
    path("specs/", APISpecsView.as_view(), name="specs"),
    path("users/", include((user_api, app_name), namespace="users")),
]
