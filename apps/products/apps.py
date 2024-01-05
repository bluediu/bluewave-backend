from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Products application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    verbose_name = "Products"

    def ready(self):
        """Extend to register custom query lookup."""
        from django.db.models import Field
        from common.models import NotEqual

        Field.register_lookup(NotEqual)
