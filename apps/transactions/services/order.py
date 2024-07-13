from typing import List, TypedDict, Required, NotRequired

from django.db import transaction
from django.utils.timezone import now
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.core.validators import ValidationError
from django.db.models import CharField, QuerySet, F, Case, When, Value, Q, Sum, Count


from apps.users.models import User
from apps.tables.models import Table
from apps.products.models import Product
from apps.transactions.models import (
    Order,
    OrderStatus,
    MAX_QUANTITY,
    MIN_QUANTITY,
)

from apps.transactions.services.payment import pending_payment_exists
from common.functions import generate_random_code


class _OrderRegisterT(TypedDict):
    """An order register type."""

    table: Required[Table]
    product: Required[Product]
    quantity: NotRequired[int]


class _BulkOrderRegisterT(TypedDict):
    """An order register type."""

    table: Required[Table]
    products: Required[List[_OrderRegisterT]]


class _OrderUpdateT(TypedDict):
    """An order update type."""

    status: NotRequired[str]
    quantity: NotRequired[int]


def _validate_order_context(user: User, fields: _OrderRegisterT) -> None:
    """Validate an order context consistency."""
    inactive_msg = "Must be active."
    if not user.is_active:
        raise ValidationError({"user": inactive_msg})

    product = fields["product"]
    if not product.is_active:
        raise ValidationError({"product": inactive_msg})

    table = fields["table"]
    if not table.is_active:
        raise ValidationError({"table": inactive_msg})

    if table.orders.not_closed().filter(product=product).exists():
        raise ValidationError(
            {
                "table": (
                    f"Product '{product.id}' already exists in an order"
                    f" for this table."
                )
            }
        )

    if pending_payment_exists(table=table):
        msg = "Forbidden action! You cannot create new order."
        raise ValidationError({"table": msg})

    if fields.get("quantity") and fields["quantity"] <= 0:
        raise ValidationError({"quantity": "Must be greater than zero."})


def get_order(order_code: str) -> Order:
    """Return an order."""
    return get_object_or_404(Order, code=order_code)


def get_order_state(table_code: str) -> dict:
    """Get order state info."""
    info = (
        Order.objects.not_closed()
        .filter(Q(table__code=table_code) & ~Q(status=OrderStatus.CANCELED))
        .aggregate(
            total_price=Sum(F("product__price") * F("quantity")),
            count_pending=Count("code", filter=Q(status=OrderStatus.PENDING)),
            count_delivered=Count("code", filter=Q(status=OrderStatus.DELIVERED)),
        )
    )

    return info


def get_order_count(table_code: str) -> dict:
    """Get order count."""
    count = Order.objects.not_closed().filter(table__code=table_code).count()
    return {"count": count}


def list_order_products(table_code: str) -> list[Order]:
    """Return a list of products for a table order."""

    order_products = (
        Order.objects.not_closed()
        .filter(table__code=table_code)
        .select_related("product", "product__category")
        .annotate(
            status_label=Case(
                *[
                    When(status=status_value, then=Value(status_label))
                    for status_value, status_label in OrderStatus.choices
                ],
                output_field=CharField(),
            ),
            product_name=F("product__name"),
            product_image=Concat(
                Value("uploads/"),
                F("product__image"),
                output_field=CharField(),
            ),
            product_price=F("product__price"),
            product_category=F("product__category__name"),
            max_qty=Value(MAX_QUANTITY),
            min_qty=Value(MIN_QUANTITY),
        )
    )

    return order_products.order_by("-status", "-created_at")


def search_orders(
    table_id: int = None,
    status: str = None,
    close: bool = False,
) -> QuerySet:
    """Return an order by table id, status, or close."""
    orders = Order.objects.select_related("table", "product", "product__category")

    if table_id:
        orders = orders.filter(table_id=table_id)
    if status:
        orders = orders.filter(status=status)
    if close:
        orders = orders.filter(is_closed=close)

    return orders.order_by("-created_at")


def register_order(*, user: User, fields: _OrderRegisterT) -> None:
    """Register an order."""
    _validate_order_context(user, fields)

    order = Order(code=generate_random_code(), **fields)
    order.full_clean()
    order.save(user.id)


@transaction.atomic
def register_bulk_orders(*, user: User, fields: _BulkOrderRegisterT) -> None:
    """Register bulk orders."""
    orders: List[Order] = []

    for item in fields["products"]:
        # Validate products integrity.
        _validate_order_context(
            user,
            fields={
                "table": fields["table"],
                "product": item["product"],
                "quantity": item["quantity"],
            },
        )

        # Define entry.
        orders.append(
            Order(
                code=generate_random_code(),
                table=fields["table"],
                product=item["product"],
                quantity=item["quantity"],
                created_at=now(),
                updated_at=now(),
                created_by=user,
                updated_by=user,
            )
        )

    # Save orders.
    Order.objects.bulk_create(objs=orders, batch_size=len(orders))


def update_order(*, order: Order, user: User, **fields: _OrderUpdateT) -> Order:
    """Update an order."""
    previous_qty = order.quantity
    previous_status = order.status
    changed_fields = order.update_fields(**fields)

    # Check payment integrity.
    if pending_payment_exists(table=order.table):
        msg = "This order can't be updated because it has a pending payment registered."
        raise ValidationError({"order": msg})

    if "status" in changed_fields and previous_status == OrderStatus.CANCELED:
        raise ValidationError({"status": "Cannot update status of a canceled order."})

    if "quantity" in changed_fields:
        if order.is_canceled:
            raise ValidationError(
                {"quantity": "Cannot update quantity of a canceled order."}
            )

        # noinspection PyTypeChecker
        if order.is_delivered and fields["quantity"] < previous_qty:
            msg = "Quantity must be greater than previous for a delivered order."
            raise ValidationError({"quantity": msg})

        # noinspection PyTypeChecker
        if order.is_delivered and fields["quantity"] > previous_qty:
            order.status = OrderStatus.PENDING
            order.save(user.id, update_fields=["status"])

    if changed_fields:
        order.full_clean()
        order.save(user.id, update_fields=changed_fields)
    return order


def close_orders_bulk(*, user: User, table: Table) -> None:
    """Close an orders."""
    orders = table.orders

    all_orders_canceled = (
        not orders.not_closed().exclude(status=OrderStatus.CANCELED).exists()
    )

    if not all_orders_canceled:
        raise ValidationError(
            {"table": "All order must be canceled to perform this operation."}
        )

    # Close associated table orders.
    orders.update(
        is_closed=True,
        updated_at=now(),
        updated_by_id=user.id,
    )
