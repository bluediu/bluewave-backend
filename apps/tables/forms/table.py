from django import forms

from apps.tables.models import Table
from common.form import is_active_field


class TableCreateForm(forms.Form):
    """A create table form schema."""

    fields_from_model = forms.fields_for_model(
        Table,
        fields=["code"],
    )


class TableUpdateForm(forms.Form):
    """A update table form schema."""

    fields_from_model = forms.fields_for_model(
        Table,
        fields=["code"],
    )
    fields_from_model["is_active"] = is_active_field(Table)["is_active"]

    def __init__(self, table_data=None, *args, **kwargs):
        """Set fields as not required."""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields_from_model.items():
            value = table_data.get(field_name, None)
            if value is not None:
                self.fields_from_model[field_name].initial = value
