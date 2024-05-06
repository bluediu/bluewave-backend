from django.db.models import Q
from django import forms

from apps.transactions.models import Order, MIN_QUANTITY, MAX_QUANTITY
from apps.products.models import Product


def get_products_choices(table_code) -> list[tuple[str, str]]:
    """Return available products as choices object."""
    # Search for products already included for an ordered table.
    not_available = Order.objects.filter(table__code=table_code).values_list(
        "product_id",
        flat=True,
    )

    products = (
        Product.objects.filter(~Q(id__in=not_available) & Q(is_active=True))
        .values_list("id", "name")
        .order_by("name")
    )
    products_choices = [("", "---------")] + list(products)
    return products_choices


class OrderRegisterForm(forms.Form):
    """A register order form schema."""

    fields_from_model = forms.fields_for_model(
        Order,
        fields=[
            "product",
            "quantity",
        ],
    )

    def __init__(self, table_code: str, *args, **kwargs):
        """Pre-fill products choices."""
        super().__init__(*args, **kwargs)

        self.fields_from_model["product"].widget.choices = get_products_choices(
            table_code
        )
        self.fields_from_model["quantity"].max_length = MAX_QUANTITY
        self.fields_from_model["quantity"].min_length = MIN_QUANTITY
