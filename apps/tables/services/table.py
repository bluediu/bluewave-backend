from typing import Literal

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet

from apps.tables.models import Table
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
