from django import forms

from apps.transactions.models import Payment


class PaymentRegisterForm(forms.Form):
    """A register payment form schema."""

    fields_from_model = forms.fields_for_model(
        Payment,
        fields=["type"],
    )
