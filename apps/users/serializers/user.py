# Libs
from rest_framework import serializers as srz

# Global
from common.serializers import Serializer


class UserInfoSerializer(Serializer):
    """A user info output serializer."""

    id = srz.IntegerField(help_text="User ID.")
    username = srz.CharField(help_text="Username.")
    first_name = srz.CharField(
        help_text="First name.",
        required=False,
    )
    last_name = srz.CharField(
        help_text="Last name.",
        required=False,
    )
    email = srz.EmailField(
        help_text="E-mail address.",
        required=False,
    )
    is_active = srz.BooleanField(help_text="Is the user active?.")
    is_staff = srz.BooleanField(help_text="Is the user staff?.")
    created_at = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class UserCreateSerializer(Serializer):
    """A user create input serializer."""

    username = srz.CharField(
        help_text="Username.",
        max_length=150,
    )
    password = srz.CharField(
        help_text=(
            "<b>Password requirement:</b> <br>"
            "<ul>"
            "<li>Your password can’t be too similar to your other personal "
            "information.</li>"
            "<li>Your password must contain at least 8 characters.</li>"
            "<li>Your password can’t be a commonly used password.</li>"
            "<li>Your password can’t be entirely numeric.</li>"
            "</ul>"
        ),
        max_length=128,
    )
    repeat_password = srz.CharField(
        help_text="Repeat password.",
        max_length=128,
    )
    first_name = srz.CharField(
        help_text="First names (optional).",
        max_length=100,
        allow_blank=True,
        required=False,
    )
    last_name = srz.CharField(
        help_text="Last names (optional).",
        max_length=100,
        allow_blank=True,
        required=False,
    )
    email = srz.EmailField(
        help_text="Contact e-mail.",
        max_length=100,
        allow_blank=True,
        required=False,
    )
    is_active = srz.BooleanField(
        help_text="Is the user active?.",
        allow_null=True,
        required=False,
    )
    is_staff = srz.BooleanField(
        help_text="Can be a user staff?.",
        allow_null=True,
        required=False,
    )


class UserUpdateSerializer(UserCreateSerializer):
    """A user update input serializer."""

    password = None
    repeat_password = None

    def __init__(self, *args, **kwargs):
        """Override default initialization."""

        super().__init__(*args, **kwargs)
        self.fields["username"].required = False
