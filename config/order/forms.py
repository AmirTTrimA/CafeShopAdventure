"""order/forms.py

This module defines the form used for submitting orders,
including validation for the phone number.
"""

from django import forms


class OrderForm(forms.Form):
    """Form for collecting customer phone number.

    Attributes:
        phone_number (str): The phone number of the customer, optional.
    """

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
