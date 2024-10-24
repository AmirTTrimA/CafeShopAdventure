"""
models.py

This module defines the Customer model for the application,
including attributes related to customer information and validation.
"""

from django.db import models
from .validator import iran_phone_regex


class Customer(models.Model):
    """
    Model representing a customer.

    Attributes:
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        phone_number (str): The phone number of the customer (validated).
        points (int): Reward points associated with the customer.
        is_active (bool): Status indicating if the customer account is active.
        created_at (datetime): The timestamp when the customer was created.
        updated_at (datetime): The timestamp when the customer was last updated.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone_number = models.CharField(
        max_length=12, validators=[iran_phone_regex], unique=True, null=True, blank=True
    )
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the full name of the customer."""
        return f"{self.first_name} {self.last_name}"
