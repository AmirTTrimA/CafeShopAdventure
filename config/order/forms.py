# order/forms.py

from django import forms
from .models import Customer
from cafe.models import Cafe
from django.core.exceptions import ValidationError


class OrderForm(forms.Form):
    """Form for collecting customer phone number and table number."""

    phone_number = forms.CharField(
        max_length=15,
        required=False,
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your phone number (optional)",
                "class": "form-control",
            }
        ),
    )

    table_number = forms.IntegerField(
        required=True,
        label="Table Number",
        widget=forms.NumberInput(
            attrs={
                "placeholder": "Enter your table number",
                "class": "form-control",
            }
        ),
    )

    cafe = forms.ModelChoiceField(
        queryset=Cafe.objects.all(), required=True, label="Select Cafe"
    )

    def clean_table_number(self):
        table_number = self.cleaned_data.get("table_number")
        cafe = self.cleaned_data.get("cafe")

        if cafe and table_number > cafe.number_of_tables:
            raise ValidationError(
                f"Table number cannot exceed {cafe.number_of_tables} for this cafe."
            )

        return table_number
