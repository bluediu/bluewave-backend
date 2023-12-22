from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Users application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = "Users"
