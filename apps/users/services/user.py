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


def get_users() -> QuerySet[User]:
    """Return the users."""
    fields = [
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
    ]
    return (
        User.objects.filter(is_superuser=False).values(*fields).order_by("-date_joined")
    )


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
    if user.is_superuser:
        raise ValidationError("Forbidden action!")
    changed_fields = user.updated_fields(**fields)
    user.updated_by = request_user
    user.full_clean()
    user.save(update_fields=changed_fields + ["updated_by", "updated_at"])
