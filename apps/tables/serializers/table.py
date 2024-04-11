from rest_framework import serializers as srz

from apps.tables.models.table import CODE_LENGTH
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


class TableCreateSerializer(Serializer):
    """A table create input serializer."""

    code = srz.CharField(
        help_text=(
            f"The table code must contain {CODE_LENGTH} numeric characters and "
            "follow a sequence pattern like '000X'."
        ),
    )


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
