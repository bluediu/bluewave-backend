from django.apps import AppConfig


class ApiConfig(AppConfig):
    """API application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.api"
    verbose_name = "APIs"
