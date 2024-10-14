"""
models.py

This module defines the Customer model for the application,
including attributes related to customer information and validation.
"""

from django.db import models
from django.core.validators import RegexValidator
# from django.contrib.auth.hashers import make_password


class Customer(models.Model):
    """
    Model representing a customer.

    Attributes:
        iran_phone_regex (RegexValidator): Validator for Iranian phone numbers.
        first_name (str): The first name of the customer.
        last_name (str): The last name of the customer.
        email (str): The email address of the customer (unique).
        password (str): The hashed password of the customer.
        phone_number (str): The phone number of the customer (validated).
        points (int): Reward points associated with the customer.
        is_active (bool): Status indicating if the customer account is active.
        created_at (datetime): The timestamp when the customer was created.
        updated_at (datetime): The timestamp when the customer was last updated.
    """

    # add this validator to a validator.py file in this app
    iran_phone_regex = RegexValidator(
        regex=r"^(\+98|0)?9\d{9}$",
        message="Phone number must be entered in the format: '+989xxxxxxxxx' or '09xxxxxxxxx'.",
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    # password = models.CharField(
    #     max_length=100
    # )  # Consider using a more secure method for password handling
    phone_number = models.CharField(max_length=12, validators=[iran_phone_regex])
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the full name of the customer."""
        return f"{self.first_name} {self.last_name}"

    # there's no need for password for customers
    # def save(self, *args, **kwargs):
    #     """Override save method to hash the password before saving."""
    #     if self.password:
    #         self.password = make_password(self.password)
    #     super(Customer, self).save(*args, **kwargs)
