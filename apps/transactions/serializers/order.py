from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers as srz

from apps.tables.serializers.table import TableInfoSerializer
from apps.products.serializers.product import ProductInfoSerializer

from apps.products.models import Product
from apps.transactions.models import MIN_QUANTITY, MAX_QUANTITY, OrderStatus
from common.serializers import Serializer


class OrderInfoSerializer(Serializer):
    """An order info output serializer."""

    code = srz.CharField(
        help_text="Order Code",
    )
    status = srz.CharField(
        help_text="Status.",
    )
    is_closed = srz.BooleanField(
        help_text="Is the order close?",
    )
    table = TableInfoSerializer(
        help_text="Table information.",
    )
    product = ProductInfoSerializer(
        help_text="Product information.",
    )
    quantity = srz.IntegerField(
        help_text="Product quantity.",
    )
    created_at = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class OrderProductsInfoSerializer(Serializer):
    """An order products info output serializer."""

    code = srz.CharField(
        help_text="Order Code.",
    )
    status_label = srz.CharField(
        help_text="Order status.",
    )
    product_id = srz.IntegerField(
        help_text="Product ID.",
    )
    product_name = srz.CharField(
        help_text="Product name.",
    )
    product_image = srz.CharField(
        help_text="Product image.",
    )
    product_category = srz.CharField(
        help_text="Product category name.",
    )
    product_price = srz.IntegerField(
        help_text="Product price.",
    )
    is_closed = srz.BooleanField(
        help_text="Is the order close?",
    )
    quantity = srz.IntegerField(
        help_text="Product quantity.",
    )
    max_qty = srz.IntegerField(
        help_text="Max product quantity (flag).",
    )
    min_qty = srz.IntegerField(
        help_text="Min product quantity (flag).",
    )
    created_at = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class OrderStateInfoSerializer(Serializer):
    """An order state output serializer."""

    count_pending = srz.IntegerField(
        help_text="Count pending orders for a table.",
    )
    total_price = srz.IntegerField(
        help_text="Calculate total product price.",
    )
    count_delivered = srz.IntegerField(
        help_text="Count delivered orders for a table.",
    )


class OrderCountSerializer(Serializer):
    """An order counting output serializer."""

    count = srz.IntegerField(
        help_text="count the number of orders associated with a table.",
    )


class OrderRegisterSerializer(Serializer):
    """An order register input serializer."""

    table = srz.CharField(
        help_text="Table Code.",
    )
    product = srz.IntegerField(
        help_text="Product ID.",
        validators=[MinValueValidator(1)],
    )
    quantity = srz.IntegerField(
        help_text="Product quantity.",
        validators=[MinValueValidator(MIN_QUANTITY), MaxValueValidator(MAX_QUANTITY)],
        required=False,
    )


class _ProductsInOrder(Serializer):
    """An product serializer (raw)."""

    product = srz.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        help_text="Product ID",
    )
    quantity = srz.IntegerField(
        help_text="Product quantity.",
        validators=[MinValueValidator(MIN_QUANTITY), MaxValueValidator(MAX_QUANTITY)],
        required=False,
    )


class OrderBulkRegisterSerializer(Serializer):
    """Bulk orders register input serializer."""

    table = srz.CharField(
        help_text="Table Code.",
    )
    products = srz.ListField(
        child=_ProductsInOrder(),
        help_text="Products item.",
    )


class OrderUpdateSerializer(Serializer):
    """An order update input serializer."""

    status = srz.ChoiceField(
        choices=OrderStatus.choices,
        help_text="Order status.",
        required=False,
    )
    quantity = srz.IntegerField(
        help_text="Product quantity.",
        validators=[MinValueValidator(MIN_QUANTITY), MaxValueValidator(MAX_QUANTITY)],
        required=False,
    )
