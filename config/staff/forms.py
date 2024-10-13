"""
forms.py

This module contains forms for the staff application, including
a custom user creation form.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating a new user with additional fields.

    This form extends the default UserCreationForm to include
    custom fields such as email and phone number.

    Attributes:
        Meta: Configuration for the form, including the model and fields.
    """

    class Meta:
        """meta"""
        model = CustomUser
        fields = ("username", "email", "phone_number", "password1", "password2")
