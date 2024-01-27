from pathlib import Path

from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator

from apps.products.models.category import Category
from common.models import BaseModel


# noinspection PyUnusedLocal
def _image_file_path(instance, filename) -> str:
    """Return a standard image path format."""
    ext = Path(filename).suffix
    filename = f"{now().strftime('%Y%m%d%H%M%S')}_{get_random_string(4)}{ext}"
    return f"products/{filename}"


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
        validators=[MinValueValidator(1)],
    )
    is_active = models.BooleanField(
        verbose_name="Active",
        default=True,
    )
    image = models.ImageField(
        verbose_name="Image",
        upload_to=_image_file_path,
        unique=True,
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "svg"])],
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
                check=models.Q(price__gte=1),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_not_empty_check",
                check=models.Q(name__ne=""),
                violation_error_message="Name can't be empty.",
            ),
        ]
