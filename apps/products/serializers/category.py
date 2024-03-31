from django.core.validators import FileExtensionValidator
from rest_framework import serializers as srz

from apps.products.types import IMAGE_EXTENSION
from common.serializers import Serializer


class CategoryInfoSerializer(Serializer):
    """A category info output serializer."""

    id = srz.IntegerField(
        help_text="Category ID",
    )
    name = srz.CharField(help_text="Category name.")
    is_active = srz.BooleanField(
        help_text="Is the category active?",
    )
    image = srz.ImageField(
        help_text="Category image.",
    )
    created_at = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class CategoryCreateSerializer(Serializer):
    """A category create input serializer."""

    name = srz.CharField(
        max_length=50,
        help_text="Category name.",
    )
    is_active = srz.BooleanField(
        help_text="Is the category active?",
        default=True,
    )
    image = srz.ImageField(
        help_text="Category image.",
        validators=[FileExtensionValidator(IMAGE_EXTENSION)],
    )


class CategoryUpdateSerializer(CategoryCreateSerializer):
    """A category update input serializer."""

    def __init__(self, *args, **kwargs):
        """Extend to make fields not required."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
