from django.apps import AppConfig


class TablesConfig(AppConfig):
    """Tables application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.tables"
    verbose_name = "Tables"

    def ready(self):
        """Extend to register custom query lookup."""
        from django.db.models import Field
        from common.models import NotEqual

        Field.register_lookup(NotEqual)
