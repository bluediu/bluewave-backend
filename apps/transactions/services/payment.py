from typing import TypedDict, Required

from django.db import transaction
from django.db.models import F, Sum
from django.utils.timezone import now
from django.core.validators import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from apps.users.models import User
from apps.tables.models import Table
from common.functions import generate_random_code
from apps.transactions.models import OrderStatus, Payment, PaymentStatus


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
            # TODO: Make this conditional
            status=PaymentStatus.PENDING,
        )
        payment.type = payment.get_type_display()
        payment.status = payment.get_status_display()
        return payment
    except ObjectDoesNotExist:
        return None


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
            code=generate_random_code(),
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
        table.orders.update(
            is_closed=True,
            updated_at=now(),
            updated_by_id=user.id,
        )
