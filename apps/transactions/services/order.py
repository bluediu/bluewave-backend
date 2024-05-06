from typing import TypedDict, Required, NotRequired

from django.shortcuts import get_object_or_404
from django.db.models import CharField, QuerySet, F, Case, When, Value, Q, Sum, Count
from django.db.models.functions import Concat
from django.core.validators import ValidationError

from apps.transactions.models import Order, OrderStatus, MAX_QUANTITY, MIN_QUANTITY
from apps.users.models import User
from apps.products.models import Product
from apps.tables.models import Table
from common.functions import generate_random_code


class _OrderCreateT(TypedDict):
    """An order create type."""

    table: Required[Table]
    product: Required[Product]
    quantity: NotRequired[int]


class _OrderUpdateT(TypedDict):
    """An order update type."""

    status: NotRequired[str]
    quantity: NotRequired[int]


def _validate_order_context(user: User, fields: _OrderCreateT) -> None:
    """Validate a order context consistency."""
    inactive_msg = "Must be active."
    if not user.is_active:
        raise ValidationError({"user": inactive_msg})

    product = fields["product"]
    if not product.is_active:
        raise ValidationError({"product": inactive_msg})

    table = fields["table"]
    if not table.is_active:
        raise ValidationError({"table": inactive_msg})

    if table.orders.filter(product=product).exists():
        raise ValidationError(
            {"table": "Product already exists in an order for this table."}
        )

    if fields.get("quantity") and fields["quantity"] <= 0:
        raise ValidationError({"quantity": _("Must be greater than zero.")})


def get_order(order_code: str) -> Order:
    """Return an order."""
    return get_object_or_404(Order, code=order_code)


def get_order_state(table_code: str) -> dict:
    """Get order state info."""
    info = Order.objects.filter(
        Q(table__code=table_code) & ~Q(status=OrderStatus.CANCELED)
    ).aggregate(
        total_price=Sum(F("product__price") * F("quantity")),
        count_pending=Count("code", filter=Q(status=OrderStatus.PENDING)),
        count_delivered=Count("code", filter=Q(status=OrderStatus.DELIVERED)),
    )

    return info


def list_order_products(table_code: str) -> list[Order]:
    """Return a list of products for a table order."""

    order_products = (
        Order.objects.filter(table__code=table_code)
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
        orders = orders.filter(is_close=close)

    return orders.order_by("-created_at")


def create_order(*, user: User, fields: _OrderCreateT) -> None:
    """Create an order."""
    _validate_order_context(user, fields)

    order = Order(code=generate_random_code(), **fields)
    order.full_clean()
    order.save(user.id)


def update_order(*, order: Order, user: User, **fields: _OrderUpdateT) -> Order:
    """Update a order."""
    previous_qty = order.quantity
    previous_status = order.status
    changed_fields = order.update_fields(**fields)

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
