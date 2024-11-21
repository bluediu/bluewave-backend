# Libs
from rest_framework import serializers as srz

# Apps
from apps.transactions.models import PaymentType

# Global
from common.serializers import Serializer


class PaymentInfoSerializer(Serializer):
    """A payment info output serializer."""

    code = srz.CharField(
        help_text="Code",
    )
    table = srz.CharField(
        help_text="Table code",
    )
    total = srz.IntegerField(
        help_text="Payment total price.",
    )
    type = srz.CharField(
        help_text="Payment type",
    )
    status = srz.CharField(
        help_text="Status",
    )
    created_at = srz.DateTimeField(
        help_text="Created at",
    )


class PaymentOrdersInfoSerializer(Serializer):
    """A payment orders info output serializer."""

    quantity = srz.IntegerField(
        help_text="Payment total price.",
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


class PaymentRegisterSerializer(Serializer):
    """A payment register input serializer."""

    table = srz.CharField(
        help_text="Table Code.",
    )
    type = srz.ChoiceField(
        help_text="Payment type.",
        choices=PaymentType.choices,
    )
