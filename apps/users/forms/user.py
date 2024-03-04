from django import forms

from apps.users.models import User
from common.form import is_active_field


# **=========== Auth ===========**
class AuthFormSchema(forms.Form):
    """An auth form schema."""

    fields_from_model = forms.fields_for_model(
        User,
        fields=["username", "password"],
        widgets={
            "password": forms.PasswordInput(),
        },
    )


# **=========== Users ===========**
class UserCreateForm(forms.Form):
    """A create customer form."""

    fields_from_model = forms.fields_for_model(
        User,
        fields=[
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        ],
        widgets={"password": forms.PasswordInput()},
    )
    fields_from_model["repeat_password"] = forms.CharField(
        label="Repeat password", widget=forms.PasswordInput()
    )


class UserUpdateForm(forms.Form):
    """A update customer form."""

    fields_from_model = forms.fields_for_model(
        User,
        fields=[
            "username",
            "first_name",
            "last_name",
            "email",
        ],
    )
    fields_from_model["is_active"] = is_active_field(User)["is_active"]

    def __init__(self, user_data=None, *args, **kwargs):
        """Extend to fill fields from user data."""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields_from_model.items():
            value = user_data.get(field_name, None)
            if value is not None:
                self.fields_from_model[field_name].initial = value
