from typing import Literal

from django.shortcuts import get_object_or_404
from django.db.models import (
    Q,
    Case,
    When,
    Count,
    Exists,
    OuterRef,
    QuerySet,
    BooleanField,
)

from apps.tables.models import Table
from apps.transactions.models import OrderStatus, Order, Payment, PaymentStatus
from apps.users.models import User


def get_table(table_id: int) -> Table:
    """Return a table."""
    return get_object_or_404(Table, id=table_id)


def get_table_by_code(table_code: str) -> Table:
    """Return a table."""
    return get_object_or_404(Table, code=table_code)


def list_tables(
    *,
    filter_by: Literal["all", "actives", "inactives"],
) -> QuerySet[Table]:
    """Return a list of tables."""
    tables = Table.objects

    if filter_by == "actives":
        tables = tables.filter(is_active=True)
    elif filter_by == "inactives":
        tables = tables.filter(is_active=False)

    return tables.order_by("id")


def list_table_order_statuses() -> dict:
    """
    Return a list of table order statuses.

    Counts the orders for each table and checks if any orders
    have been delivered, indicating that the table is busy.
    """
    tables = (
        Table.objects.values("id", "code")
        .annotate(
            orders_number=Count(
                "orders",
                filter=Q(
                    orders__status=OrderStatus.PENDING,
                    orders__is_close=False,
                ),
            ),
            all_orders_delivered=Case(
                When(
                    orders_number=0,
                    then=Exists(
                        Order.objects.filter(
                            table_id=OuterRef("id"),
                            status=OrderStatus.DELIVERED,
                            is_close=False,
                        )
                    ),
                ),
                default=False,
                output_field=BooleanField(),
            ),
            all_orders_canceled=Case(
                When(
                    # Check if there are any non-closed orders for the table.
                    Exists(
                        Order.objects.filter(
                            table_id=OuterRef("id"),
                            is_close=False,
                        )
                    ),
                    # If there are non-closed orders, check if all of them are canceled.
                    then=~Exists(
                        Order.objects.filter(
                            table_id=OuterRef("id"),
                            is_close=False,
                        ).exclude(status=OrderStatus.CANCELED)
                    ),
                ),
                # If there are no non-closed orders, set to False.
                default=False,
                output_field=BooleanField(),
            ),
            pending_payment=Exists(
                Payment.objects.filter(
                    table_id=OuterRef("id"),
                    status=PaymentStatus.PENDING,
                )
            ),
        )
        .filter(is_active=True)
        .order_by("code")
    )

    return tables


def create_table(*, user: User, **fields: dict) -> Table:
    """Create a table."""
    table = Table(**fields)
    table.full_clean()
    table.save(user.id)
    return table


def update_table(*, table: Table, user: User, **fields: dict) -> Table:
    """Update a table."""
    changed_fields = table.update_fields(**fields)
    if changed_fields:
        table.full_clean()
        table.save(user.id, update_fields=changed_fields)
    return table
