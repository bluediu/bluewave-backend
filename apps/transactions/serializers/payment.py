from rest_framework import serializers as srz

from apps.transactions.models import PaymentType
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


class PaymentRegisterSerializer(Serializer):
    """A payment register input serializer."""

    table = srz.CharField(
        help_text="Table Code.",
    )
    type = srz.ChoiceField(
        help_text="Payment type.",
        choices=PaymentType.choices,
    )
