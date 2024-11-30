# Core
from pathlib import Path

# Libs
from django.db import models
from django.utils.timezone import now
from django.utils.crypto import get_random_string
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)

# Apps
from apps.products.models.category import Category
from apps.products.types import IMAGE_EXTENSION

# Global
from common.models import BaseModel
from common.functions import cents_to_dollar, clean_spaces


# noinspection PyUnusedLocal
def _image_file_path(instance, filename) -> str:
    """Return a standard image path format."""

    ext = Path(filename).suffix
    filename = f"{now().strftime('%Y%m%d%H%M%S')}_{get_random_string(4)}{ext}"
    return f"products/{filename}"


MAX_PRICE = 10000  # $100 usd
MIN_PRICE = 100  # $1.00 usd


class Product(BaseModel):
    """A product db model."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Name",
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
    )
    price = models.IntegerField(
        verbose_name="Price",
        validators=[MinValueValidator(MIN_PRICE), MaxValueValidator(MAX_PRICE)],
        help_text=(
            f"The price of the product must be between"
            f" ${cents_to_dollar(cents=MIN_PRICE)} "
            f"USD and "
            f"${cents_to_dollar(cents=MAX_PRICE)} USD."
        ),
    )
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
    )
    image = models.ImageField(
        verbose_name="Image",
        upload_to=_image_file_path,
        unique=True,
        validators=[FileExtensionValidator(IMAGE_EXTENSION)],
    )
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.PROTECT,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Product"
        verbose_name_plural = "Products"
        permissions = [
            ("create_product", "Create product"),
            ("list_product", "List product"),
            ("view_product", "View product"),
            ("change_product", "Change product"),
        ]
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_price_check",
                check=models.Q(price__gte=MIN_PRICE),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_not_empty_check",
                check=models.Q(name__ne=""),
                violation_error_message="Name can't be empty.",
            ),
        ]

    def clean(self):
        """Clean product fields."""

        self.name = clean_spaces(self.name.capitalize())
        self.description = clean_spaces(self.description.capitalize())

    def __str__(self) -> str:
        """Return instance name."""

        return self.name
