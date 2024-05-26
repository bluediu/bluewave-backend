from typing import Literal

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.core.validators import ValidationError
from django.core.files.storage import default_storage

from apps.products.models import Product
from apps.users.models import User


def get_product(product_id: int) -> Product:
    """Return a product."""
    return get_object_or_404(Product, id=product_id)


def list_products(
    *,
    filter_by: Literal["all", "actives", "inactives"],
) -> QuerySet[Product]:
    """Return a list of products."""
    products = Product.objects.select_related("category")

    if filter_by == "actives":
        products = products.filter(is_active=True)
    elif filter_by == "inactives":
        products = products.filter(is_active=False)

    return products.order_by("id")


def create_product(*, user: User, **fields: dict) -> Product:
    """Create a product."""
    product = Product(**fields)
    product.full_clean()
    product.save(user.id)
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
        return product
