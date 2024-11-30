# Libs
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator

# Apps
from apps.tables.models import Table

# Global
from common.models import BaseModel


class PaymentType(models.TextChoices):
    """Payment type."""

    CASH = "CASH", "Cash"
    CARD = "CARD", "Card"


class PaymentStatus(models.TextChoices):
    """Payment status."""

    PENDING = "PENDING", "Pending"
    PAID = "PAID", "Paid"


CODE_LENGTH = 6
MIN_TOTAL = 100  # $1.00 usd


class Payment(BaseModel):
    """A payment db model."""

    code = models.CharField(
        primary_key=True,
        unique=True,
        validators=[
            RegexValidator(f"^[0-9A-Za-z]{{{CODE_LENGTH}}}$"),
        ],
        max_length=CODE_LENGTH,
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.PROTECT,
        related_name="payments",
    )
    total = models.IntegerField(
        verbose_name="Total price",
        validators=[MinValueValidator(MIN_TOTAL)],
    )
    type = models.TextField(
        verbose_name="Payment type",
        choices=PaymentType.choices,
    )
    status = models.TextField(
        verbose_name="Status",
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        permissions = [
            ("create_payment", "Create payment"),
            ("list_payment", "List payment"),
            ("view_payment", "View payment"),
            ("change_payment", "Change payment"),
        ]
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_code_valid",
                check=models.Q(code__regex=f"^[0-9A-Za-z]{{{CODE_LENGTH}}}$"),
                violation_error_message="Invalid code.",
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_total_check",
                check=models.Q(total__gte=MIN_TOTAL),
            ),
        ]
