from django import forms
from django.utils.timezone import localdate

from apps.transactions.models import PaymentType
from apps.transactions.models import Payment

from common.validators import NumericStringValidator


class PaymentRegisterForm(forms.Form):
    """A register payment form schema."""

    fields_from_model = forms.fields_for_model(
        Payment,
        fields=["type"],
    )


class PaymentSearchForm(forms.Form):
    """Search payment form."""

    payment_type = forms.ChoiceField(
        label="Payment type",
        choices=PaymentType.choices + [("ALL", "All")],
        required=True,
    )
    code = forms.CharField(
        label="Table code",
        required=False,
        validators=[NumericStringValidator()],
    )
    since = forms.DateField(
        label="Since",
        required=False,
    )
    until = forms.DateField(
        label="Unit",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """Extend to customize and validate fields."""
        super().__init__(*args, **kwargs)

        # Set 'max' attribute for date fields to current local date
        current_date = localdate()
        self.fields["since"].widget.attrs["max"] = current_date
        self.fields["since"].widget.attrs["min"] = ""
        self.fields["until"].widget.attrs["max"] = current_date
        self.fields["until"].widget.attrs["min"] = ""
