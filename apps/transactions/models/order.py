from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)

from apps.tables.models import Table
from apps.products.models import Product
from common.models import BaseModel


class OrderStatus(models.TextChoices):
    """Order status."""

    PENDING = "PENDING", "Pending"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELED = "CANCELED", "Canceled"


CODE_LENGTH = 6
MAX_QUANTITY = 7
MIN_QUANTITY = 1


class Order(BaseModel):
    """An order db model."""

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
        related_name="orders",
        on_delete=models.PROTECT,
    )
    product = models.ForeignKey(
        Product,
        related_name="orders",
        on_delete=models.PROTECT,
    )
    quantity = models.IntegerField(
        verbose_name="Price",
        validators=[MinValueValidator(MIN_QUANTITY), MaxValueValidator(MAX_QUANTITY)],
        default=MIN_QUANTITY,
        help_text=(
            f"The product quantity must be between "
            f"{MIN_QUANTITY} and {MAX_QUANTITY}"
        ),
    )
    # todo: Add payment model FK
    status = models.TextField(
        verbose_name="Status",
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    is_close = models.BooleanField(
        verbose_name="Is the order close?",
        default=False,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        permissions = [
            ("create_order", "Create order"),
            ("list_order", "List orders"),
            ("view_order", "View order"),
            ("change_order", "Update order"),
        ]
        constraints = [
            # TODO: add constrain based on status
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_code_valid",
                check=models.Q(code__regex=f"^[0-9A-Za-z]{{{CODE_LENGTH}}}$"),
                violation_error_message="Invalid code.",
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_quantity_check",
                check=models.Q(quantity__gte=MIN_QUANTITY)
                & models.Q(quantity__lte=MAX_QUANTITY),
                violation_error_message="Invalid quantity.",
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_status_valid",
                check=models.Q(status__in=OrderStatus.values),
                violation_error_message="Invalid status.",
            ),
        ]
