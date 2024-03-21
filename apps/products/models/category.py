from pathlib import Path

from django.utils.crypto import get_random_string
from django.utils.timezone import now
from django.db import models
from django.core.validators import FileExtensionValidator

from common.models import BaseModel
from common.functions import clean_spaces
from apps.products.types import IMAGE_EXTENSION


# noinspection PyUnusedLocal
def _image_file_path(instance, filename) -> str:
    """Return a standard image path format."""
    ext = Path(filename).suffix
    filename = f"{now().strftime('%Y%m%d%H%M%S')}_{get_random_string(4)}{ext}"
    return f"categories/{filename}"


class Category(BaseModel):
    """A category db model."""

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Name",
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

    class Meta(BaseModel.Meta):
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        permissions = [
            ("create_category", "Create category"),
            ("list_category", "List category"),
            ("view_category", "View category"),
            ("change_category", "Change category"),
        ]
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_name_not_empty_check",
                check=models.Q(name__ne=""),
                violation_error_message="Name can't be empty.",
            )
        ]

    def clean(self):
        """Clean category fields."""
        self.name = clean_spaces(self.name.capitalize())
