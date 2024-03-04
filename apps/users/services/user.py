from enum import Enum
from typing import Literal

from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.users.models.user import User


def _check_password_match(fields: dict) -> None:
    """Check passwords' integrity."""
    if fields["password"] != fields["repeat_password"]:
        raise ValidationError({"password": "Password does not match"})

    fields.pop("repeat_password")


def get_user(user_id: int) -> User:
    """Return a user."""
    return get_object_or_404(User, id=user_id)


class FilterOpt(Enum):
    """Filter options for users."""

    ACTIVES = "actives"
    INACTIVES = "inactives"


def get_users(
    *,
    user: User,
    filter_by: Literal["all", "actives", "inactives"] = "all",
) -> QuerySet[User]:
    """Return the users."""
    users = User.objects.values(
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "created_at",
        "updated_at",
    )

    # Only a superuser can see another superusers.
    if not user.is_superuser:
        users = users.filter(is_superuser=False)

    if filter_by == FilterOpt.ACTIVES.value:
        users = users.filter(is_active=True)
    elif filter_by == FilterOpt.INACTIVES.value:
        users = users.filter(is_active=False)

    return users.order_by("id")


def create_user(*, request_user: User, **fields: dict) -> User:
    """Create a user."""
    _check_password_match(fields)
    # Encrypt password using algorithm `pbkdf2_sha256`.
    fields["password"] = make_password(fields["password"])
    user = User(**fields, created_by=request_user, updated_by=request_user)
    user.full_clean()
    user.save()
    return user


def update_user(*, user: User, request_user: User, **fields: dict) -> None:
    """Update a user."""
    if not request_user.is_superuser and user.is_superuser:
        raise ValidationError("Only a superuser can update another superuser.")
    changed_fields = user.updated_fields(**fields)
    user.updated_by = request_user
    user.full_clean()
    user.save(update_fields=changed_fields + ["updated_by", "updated_at"])
