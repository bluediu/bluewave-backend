# Libs
from django import forms

# Apps
from apps.products.models import Category

# Global
from common.form import is_active_field


class CategoryCreateForm(forms.Form):
    """A create category form schema."""

    fields_from_model = forms.fields_for_model(
        Category,
        fields=["name", "image"],
    )


class CategoryUpdateForm(forms.Form):
    """A update category form schema."""

    fields_from_model = forms.fields_for_model(
        Category,
        fields=["name", "image"],
    )
    fields_from_model["is_active"] = is_active_field(Category)["is_active"]

    def __init__(self, category_data=None, *args, **kwargs):
        """Set fields as not required."""

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields_from_model.items():
            value = category_data.get(field_name, None)
            if value is not None:
                self.fields_from_model[field_name].initial = value
