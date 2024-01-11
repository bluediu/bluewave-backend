from django.db import models
from django.core.validators import FileExtensionValidator

from common.models import BaseModel
from common.functions import image_file_path


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
        upload_to=image_file_path,
        unique=True,
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "svg"])],
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
