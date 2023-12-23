from drf_spectacular import views


class APISchemaView(views.SpectacularAPIView):
    """API schema view."""


class APISpecsView(views.SpectacularRedocView):
    """API specifications view."""

    url_name = "api:schema"
