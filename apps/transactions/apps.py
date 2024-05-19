from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """Transactions application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.transactions"
    verbose_name = "Transactions"
