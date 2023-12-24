from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models

from common.functions import clean_spaces


class User(AbstractUser):
    """A custom user."""

    created_at = models.DateTimeField(
        verbose_name="Created at",
        auto_now=True,
    )
    created_by = models.ForeignKey(
        "User",
        verbose_name="Created by",
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_created_by",
        related_query_name="%(app_label)s_%(class)s_created_by",
        editable=False,
        null=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
    )
    updated_by = models.ForeignKey(
        "User",
        verbose_name="Updated by",
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_updated_by",
        related_query_name="%(app_label)s_%(class)s_updated_by",
        editable=False,
        null=True,
    )

    def clean(self):
        """Clean user fields."""
        super().clean()

        self.username = clean_spaces(self.username.lower())
        self.first_name = clean_spaces(self.first_name)
        self.last_name = clean_spaces(self.last_name)

    def updated_fields(self, **fields: Any) -> list[str]:
        """Return a list of the changed fields."""
        changed_fields = []
        for field, value in fields.items():
            if getattr(self, field) != value:
                setattr(self, field, value)
                changed_fields.append(field)
        return changed_fields
