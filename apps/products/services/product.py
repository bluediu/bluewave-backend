from typing import Literal

from django.db import transaction
from django.db.models import QuerySet, Value
from django.shortcuts import get_object_or_404
from django.core.validators import ValidationError
from django.core.files.storage import default_storage

from apps.products.models import Product
from apps.users.models import User
from apps.transactions.models import (
    MAX_QUANTITY,
    MIN_QUANTITY,
)


def _add_qty_props(product: Product) -> Product:
    """Add quantity properties to product."""
    product.max_qty = MAX_QUANTITY
    product.min_qty = MIN_QUANTITY
    return product


def get_product(product_id: int) -> Product:
    """Return a product."""
    product = get_object_or_404(Product, id=product_id)
    product = _add_qty_props(product)
    return product


def list_products(
    *,
    filter_by: Literal["all", "actives", "inactives"],
    category: int | None = None,
) -> QuerySet[Product]:
    """Return a list of products."""
    products = Product.objects.select_related("category").annotate(
        max_qty=Value(MAX_QUANTITY),
        min_qty=Value(MIN_QUANTITY),
    )

    if filter_by == "actives":
        products = products.filter(is_active=True)
    elif filter_by == "inactives":
        products = products.filter(is_active=False)

    if category is not None:
        products = products.filter(category=category)

    return products.order_by("id")


def list_latest_products() -> QuerySet[Product]:
    """Return a list of 5 latest products."""
    fields = ["id", "name", "image", "created_at"]
    # Use `only` to return instances.
    products = Product.objects.only(*fields).order_by("-created_at")[:5]
    return products


def create_product(*, user: User, **fields: dict) -> Product:
    """Create a product."""
    product = Product(**fields)
    product.full_clean()
    product.save(user.id)
    product = _add_qty_props(product)
    return product


def update_product(*, product: Product, user: User, **fields: dict) -> Product:
    """Update a product."""
    existing_image = product.image.name

    in_process_transaction = product.orders.not_closed().exists()
    if in_process_transaction:
        msg = (
            "This product can't be edited because it is currently "
            "in a pending transaction."
        )
        raise ValidationError({"product": msg})

    with transaction.atomic():
        changed_fields = product.update_fields(**fields)
        if changed_fields:
            if "image" in changed_fields:
                if default_storage.exists(existing_image):
                    default_storage.delete(existing_image)
            product.full_clean()
            product.save(user.id, update_fields=changed_fields)
        product = _add_qty_props(product)
        return product
