from django import forms
from django.forms import fields_for_model


def clean_spaces(content: str) -> str:
    """Remove spaces from a string."""
    return " ".join(content.split())


def form_to_api_schema(*, form: fields_for_model) -> dict:
    """Convert a form schema to a JSON schema."""
    fields_data = []

    for name, field in form.fields_from_model.items():
        type_mapping = {
            forms.TextInput: "text",
            forms.EmailField: "email",
            forms.PasswordInput: "password",
            forms.BooleanField: "checkbox",
            forms.Select: "select",
            forms.Textarea: "textarea",
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
                {"value": choice[0], "label": choice[1]}
                for choice in getattr(field, "choices", [])
            ],
            "value": field.initial,
        }
        fields_data.append(field_info)

    return {"fields": fields_data}
