from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)
from rest_framework import serializers as srz

from apps.products.serializers.category import CategoryInfoSerializer
from apps.products.types import IMAGE_EXTENSION
from apps.products.models import MIN_PRICE, MAX_PRICE
from common.serializers import Serializer


class ProductInfoSerializer(Serializer):
    """A product info output serializer."""

    id = srz.IntegerField(
        help_text="Product ID",
    )
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
    created_at = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class ProductLatestInfoSerializer(Serializer):
    """A product latest info output serializer."""

    id = srz.IntegerField(
        help_text="Product ID",
    )
    name = srz.CharField(
        help_text="Product name.",
    )
    image = srz.ImageField(
        help_text="Product image.",
    )


class ProductDetailSerializer(ProductInfoSerializer):
    """A product detail output serializer."""

    max_qty = srz.IntegerField(
        help_text="Max. quantity of product in an order.",
    )
    min_qty = srz.IntegerField(
        help_text="Min. quantity of product in an order.",
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
        validators=[MinValueValidator(MIN_PRICE), MaxValueValidator(MAX_PRICE)],
    )
    is_active = srz.BooleanField(
        help_text="Is product active?",
        default=True,
    )
    image = srz.ImageField(
        help_text="Product image.",
        validators=[FileExtensionValidator(IMAGE_EXTENSION)],
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
