# Core
from typing import TypedDict, Required

# Libs
from django.db import transaction
from django.utils.timezone import now
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.core.validators import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, F, Sum, Value, CharField

# Apps
from apps.users.models import User
from apps.tables.models import Table
from apps.tables.services.table import get_table_by_code
from apps.transactions.models import Order, OrderStatus, Payment, PaymentStatus

# Global
from common import functions as fn


class _PaymentRegisterT(TypedDict):
    """A payment register type."""

    table: Required[Table]
    type: Required[str]


def pending_payment_exists(*, table: Table) -> bool:
    """Search for pending payment for a table."""

    pending_payment = Payment.objects.filter(
        table=table,
        status=PaymentStatus.PENDING,
    ).exists()

    return pending_payment


def _validate_payment_context(user: User, fields: _PaymentRegisterT) -> None:
    """Validate a payment context consistency."""

    inactive_msg = "Must be active."
    if not user.is_active:
        raise ValidationError({"user": inactive_msg})

    table = fields["table"]
    if not table.is_active:
        raise ValidationError({"table": inactive_msg})

    if pending_payment_exists(table=table):
        msg = "Forbidden action! Already exists a pending payment."
        raise ValidationError({"table": msg})

    table_orders = table.orders
    if not table_orders.exists():
        raise ValidationError({"table": "No orders to process."})
    if table_orders.filter(status=OrderStatus.PENDING).exists():
        msg = "All orders/products must be `delivered` for a payment transaction."
        raise ValidationError({"table": msg})


def get_payment(table_code: str) -> Payment | None:
    """Return a payment."""

    try:
        payment = Payment.objects.get(
            table__code=table_code,
            status=PaymentStatus.PENDING,
        )
        payment.type = payment.get_type_display()
        payment.status = payment.get_status_display()
        return payment
    except ObjectDoesNotExist:
        return None


def list_orders_by_payment(code: str) -> QuerySet[Order]:
    """Return a list of orders by payment."""

    payment = get_object_or_404(Payment, pk=code)
    orders = (
        payment.orders.filter(is_closed=True)
        .only("quantity", "product")
        .annotate(
            product_name=F("product__name"),
            product_image=Concat(
                Value("uploads/"),
                F("product__image"),
                output_field=CharField(),
            ),
            product_price=F("product__price"),
            product_category=F("product__category__name"),
        )
    )

    return orders


def search_payments(
    payment_type: str = "ALL",
    code: str = None,
    since: str = None,
    until: str = None,
) -> QuerySet[Payment]:
    """Return a list of payments."""

    payments = Payment.objects.filter(status=PaymentStatus.PAID)

    if code:
        code = get_table_by_code(code)
        payments = payments.filter(table__code=code)
    if payment_type != "ALL":
        payments = payments.filter(type=payment_type)
    if since and until:
        payments = payments.filter(
            created_at__date__range=[
                fn.parse_date(since),
                fn.parse_date(until),
            ]
        )

    return payments.order_by("-created_at")


def register_payment(*, user: User, fields: _PaymentRegisterT) -> None:
    """Register a payment."""

    _validate_payment_context(user, fields)

    with transaction.atomic():
        orders = fields.get("table").orders

        # Calculate orders total price.
        total_price = (
            orders.not_closed()
            .filter(
                status=OrderStatus.DELIVERED,
            )
            .aggregate(total_price=Sum(F("product__price") * F("quantity")))[
                "total_price"
            ]
        )

        # Save payment.
        payment = Payment(
            code=fn.generate_random_code(),
            total=total_price,
            **fields,
        )
        payment.full_clean()
        payment.save(user.id)


def close_payment(*, user: User, table: Table) -> None:
    """Close a payment."""

    with transaction.atomic():
        # Change payment status.
        pending_payment = table.payments.get(status=PaymentStatus.PENDING)
        pending_payment.status = PaymentStatus.PAID
        pending_payment.save(user.id, update_fields=["status"])

        # Close associated table orders.
        table.orders.not_closed().update(
            is_closed=True,
            payment=pending_payment,
            updated_at=now(),
            updated_by_id=user.id,
        )
