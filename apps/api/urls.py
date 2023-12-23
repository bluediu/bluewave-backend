from django.urls import include, path

from apps.api.views import APISchemaView, APISpecsView


app_name = "api"

urlpatterns = [
    path("schema/", APISchemaView.as_view(), name="schema"),
    path("specs/", APISpecsView.as_view(), name="specs"),
]
