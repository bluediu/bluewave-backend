from django import forms

from apps.products.models import Product, Category, MIN_PRICE, MAX_PRICE
from common.form import is_active_field
from common.functions import cents_to_dollar


def get_category_choices() -> list[tuple[str, str]]:
    """Return categories as choices object."""
    categories = (
        Category.objects.filter(is_active=True)
        .values_list("id", "name")
        .order_by("name")
    )
    categories_choices = [("", "---------")] + list(categories)

    return categories_choices


class ProductCreateForm(forms.Form):
    """A create product form schema."""

    fields_from_model = forms.fields_for_model(
        Product,
        fields=[
            "name",
            "description",
            "price",
            "image",
            "category",
        ],
    )

    def __init__(self, *args, **kwargs):
        """Change fields structure."""
        super().__init__(*args, **kwargs)

        self.fields_from_model["category"].widget.choices = get_category_choices()

        # Set price values
        self.fields_from_model["price"].initial = MIN_PRICE // 100
        self.fields_from_model["price"].max_length = MAX_PRICE // 100
        self.fields_from_model["price"].min_length = MIN_PRICE // 100


class ProductUpdateForm(ProductCreateForm):
    """A update product form schema."""

    fields_from_model = forms.fields_for_model(
        Product,
        fields=[
            "name",
            "description",
            "price",
            "image",
            "category",
        ],
    )
    fields_from_model["is_active"] = is_active_field(Product)["is_active"]

    def __init__(self, product_data=None, *args, **kwargs):
        """Change fields structure."""
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields_from_model.items():
            value = product_data.get(field_name, None)
            if field_name == "price":
                value = cents_to_dollar(cents=value)
            if value is not None:
                self.fields_from_model[field_name].initial = value

        self.fields_from_model["category"].widget.choices = get_category_choices()
