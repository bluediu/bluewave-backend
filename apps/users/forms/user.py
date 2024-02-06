from django import forms

from apps.users.models import User


class AuthFormSchema(forms.Form):
    """An auth form schema."""

    fields_from_model = forms.fields_for_model(
        User,
        fields=["username", "password"],
        widgets={
            "password": forms.PasswordInput(),
        },
    )
