from django.db import models
from django.core.exceptions import ValidationError

from common.models import BaseModel

CODE_LENGTH = 4


class Table(BaseModel):
    """A tables db model."""

    code = models.CharField(
        verbose_name="Code",
        max_length=CODE_LENGTH,
        help_text=(
            f"The table code must contain {CODE_LENGTH} numeric characters and "
            "follow a sequence pattern like '000X'."
        ),
        unique=True,
    )
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Table"
        verbose_name_plural = "Tables"
        permissions = [
            ("create_table", "Create table"),
            ("list_table", "List table"),
            ("view_table", "View table"),
            ("change_table", "Change table"),
        ]
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_code_not_empty_check",
                check=models.Q(code__ne=""),
                violation_error_message="Code can't be empty.",
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_code_valid",
                check=models.Q(code__regex="^[0-9]+$"),
            ),
        ]

    def __str__(self) -> str:
        """Return a string description."""
        return self.code

    def clean(self) -> None:
        """Clean some stuff."""

        if not self.code.isnumeric():
            raise ValidationError({"code": "Value must be numeric."})
        if len(self.code) < CODE_LENGTH:
            raise ValidationError(
                {"code": f"Value must be at least {CODE_LENGTH} characters."}
            )
