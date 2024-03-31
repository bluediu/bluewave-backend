from typing import Literal

from django import forms
from django.http import QueryDict
from django.forms import fields_for_model
from django.core.validators import ValidationError


def clean_spaces(content: str) -> str:
    """Remove spaces from a string."""
    return " ".join(content.split())


def cents_to_dollar(*, cents: int) -> str | None:
    """Convert cents to dollars."""
    if cents is not None:
        dollar = cents / 100.0
        return f"{dollar:0.2f}"
    return None


def form_to_api_schema(*, form: fields_for_model) -> dict:
    """Convert a form schema to a JSON schema."""
    fields_data = []

    def set_field_value(*, field_value: fields_for_model):
        """
        Set the value for a field.

        When the field is a file, a default value will be used.
        If the field has an initial value, it will be returned.
        Otherwise, the empty value for the field will be returned.
        """
        is_file = isinstance(field.widget, forms.ClearableFileInput)
        has_initial_value = field_value.initial is not None

        if is_file and has_initial_value:
            return f"/uploads/{field_value.initial}"
        elif has_initial_value:
            return field_value.initial
        else:
            return getattr(field_value, "empty_value", "")

    for name, field in form.fields_from_model.items():
        type_mapping = {
            forms.TextInput: "text",
            forms.EmailInput: "email",
            forms.PasswordInput: "password",
            forms.BooleanField: "checkbox",
            forms.Select: "select",
            forms.Textarea: "textarea",
            forms.ClearableFileInput: "file",
            forms.NumberInput: "number",
        }

        widget_type = type_mapping.get(field.widget.__class__, "unknown")
        field_info = {
            "type": widget_type,
            "name": name,
            "label": field.label,
            "help_text": field.help_text,
            "disabled": field.disabled,
            "validations": [
                {
                    "required": field.required,
                    "max_length": (
                        field.max_length if hasattr(field, "max_length") else None
                    ),
                    "min_length": (
                        field.min_length if hasattr(field, "min_length") else None
                    ),
                }
            ],
            "choices": [
                {
                    "key": str(choice[0]).lower(),
                    "value": str(choice[0]).lower(),
                    "text": choice[1],
                }
                for choice in getattr(field.widget, "choices", [])
            ],
            "value": set_field_value(field_value=field),
        }
        fields_data.append(field_info)

    return {"fields": fields_data}


VALID_FILTERS = ("all", "actives", "inactives")


def validate_filter_query_param(
    query_params: QueryDict,
) -> Literal["all", "actives", "inactives"]:
    """Return validated query filter param."""
    filter_by = query_params.get("filter_by", "all")
    if filter_by not in VALID_FILTERS:
        raise ValidationError({"filter_by": "invalid choice."})
    return filter_by
