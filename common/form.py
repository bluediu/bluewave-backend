from functools import partial
from django import forms


is_active_field = partial(
    forms.fields_for_model,
    fields=["is_active"],
    widgets={"is_active": forms.Select(choices=[(True, "Yes"), (False, "No")])},
    help_texts={"is_active": ""},
)
