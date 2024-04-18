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
from apps.transactions.models import OrderStatus, Order
from apps.users.models import User


def get_table(table_id: int) -> Table:
    """Return a table."""
    return get_object_or_404(Table, id=table_id)


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
                filter=Q(orders__status=OrderStatus.PENDING),
            ),
            all_orders_delivered=Case(
                When(
                    orders__gt=0,
                    then=~Exists(
                        Order.objects.filter(table_id=OuterRef("id")).exclude(
                            status=OrderStatus.DELIVERED,
                        )
                    ),
                ),
                default=False,
                output_field=BooleanField(),
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
