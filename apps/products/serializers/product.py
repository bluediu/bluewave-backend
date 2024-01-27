from django.core.validators import MinValueValidator, FileExtensionValidator
from rest_framework import serializers as srz

from apps.products.serializers.category import CategoryInfoSerializer
from common.serializers import Serializer


class ProductInfoSerializer(Serializer):
    """A product info output serializer."""

    name = srz.CharField(
        help_text="Product name.",
    )
    description = srz.CharField(
        help_text="Product description.",
    )
    price = srz.IntegerField(
        help_text="Price in dollar cents.",
    )
    is_active = srz.BooleanField(
        help_text="Is product active?",
    )
    image = srz.ImageField(
        help_text="Product image.",
    )
    category = CategoryInfoSerializer(
        help_text="Product category information.",
    )


class ProductCreateSerializer(Serializer):
    """A product create input serializer."""

    name = srz.CharField(
        max_length=50,
        help_text="Product name.",
    )
    description = srz.CharField(
        help_text="Product description.",
        allow_blank=True,
        required=False,
    )
    price = srz.IntegerField(
        help_text=(
            "Price in whole dollar cents. Only integer values are accepted;"
            " any decimal values will be ignored."
        ),
        validators=[MinValueValidator(1000)],
    )
    is_active = srz.BooleanField(
        help_text="Is product active?",
        default=True,
    )
    image = srz.ImageField(
        help_text="Product image.",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "svg"])],
    )
    category = srz.IntegerField(
        help_text="Category ID.",
        validators=[MinValueValidator(1)],
    )


class ProductUpdateSerializer(ProductCreateSerializer):
    """A product update input serializer."""

    def __init__(self, *args, **kwargs):
        """Extend to make fields not required."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
