from rest_framework import serializers as srz

from apps.tables.models import CODE_LENGTH
from common.serializers import Serializer


class TableInfoSerializer(Serializer):
    """A table info output serializer."""

    id = srz.IntegerField(
        help_text="Table ID",
    )
    code = srz.CharField(
        help_text="Code",
    )
    is_active = srz.BooleanField(
        help_text="Is table active?",
    )
    created_at = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class TableLoginTokenSerializer(Serializer):
    """A table info output serializer."""

    access = srz.CharField(
        help_text="Authentication access token.",
    )
    code = srz.CharField(
        help_text="Table code",
    )


class TableOrderStatusSerializer(Serializer):
    """A table order status output serializer."""

    id = srz.IntegerField(
        help_text="Table ID",
    )
    code = srz.CharField(
        help_text="Code",
    )
    orders_number = srz.IntegerField(
        help_text="Number of orders by table.",
    )
    all_orders_delivered = srz.BooleanField(
        help_text="Have all the orders for a table been delivered?"
    )
    all_orders_canceled = srz.BooleanField(
        help_text="Have all the orders for a table been canceled?"
    )
    pending_payment = srz.BooleanField(
        help_text="Indicates if a table has a pending payment.,"
    )


class TableCreateSerializer(Serializer):
    """A table create input serializer."""

    code = srz.CharField(
        help_text=(
            f"The table code must contain {CODE_LENGTH} numeric characters and "
            "follow a sequence pattern like '000X'."
        ),
    )


class TableLoginSerializer(Serializer):
    """A table login input serializer."""

    code = srz.CharField()


class TableUpdateSerializer(TableCreateSerializer):
    """A table update input serializer."""

    is_active = srz.BooleanField(
        help_text="Is the table active?",
        default=True,
    )

    def __init__(self, *args, **kwargs):
        """Extend to make fields not required."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
