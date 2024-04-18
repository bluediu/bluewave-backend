from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """Orders application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.transactions"
    verbose_name = "Orders"
