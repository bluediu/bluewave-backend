from typing import Literal

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.core.validators import ValidationError
from django.core.files.storage import default_storage

from apps.products.models import Category
from apps.transactions.models import Order
from apps.users.models import User


def get_category(category_id: int) -> Category:
    """Return a category."""
    return get_object_or_404(Category, id=category_id)


def list_categories(
    *, filter_by: Literal["all", "actives", "inactives"]
) -> QuerySet[Category]:
    """Return a list of categories."""
    categories = Category.objects

    if filter_by == "actives":
        categories = categories.filter(is_active=True)
    elif filter_by == "inactives":
        categories = categories.filter(is_active=False)

    return categories.order_by("id")


def create_category(*, user: User, **fields: dict) -> Category:
    """Create a category."""
    category = Category(**fields)
    category.full_clean()
    category.save(user.id)
    return category


def update_category(*, category: Category, user: User, **fields: dict) -> Category:
    """Update a category."""
    in_process_transaction = Order.objects.not_closed().filter(
        product_id__in=category.products.values_list("id", flat=True),
    )

    if in_process_transaction:
        msg = (
            "This category cannot be edited because one of your "
            "products is currently in a pending transaction."
        )
        raise ValidationError({"category": msg})

    existing_image = category.image.name
    with transaction.atomic():
        changed_fields = category.update_fields(**fields)
        if changed_fields:
            if "image" in changed_fields:
                if default_storage.exists(existing_image):
                    default_storage.delete(existing_image)
            category.full_clean()
            category.save(user.id)
        return category
