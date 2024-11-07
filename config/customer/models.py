"""
models.py

This module defines the Customer model for the application,
including attributes related to customer information and validation.
"""

from django.db import models
from django.core.exceptions import ValidationError
from cafe.models import Cafe
from .validator import iran_phone_regex
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

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    table_number = models.PositiveIntegerField()
    # Doesn't need these two fields for now
    # date_of_birth =models.DateField(null=True,blank=True)
    # gender =models.CharField(max_length=10,choices=gender_choices,null=True,blank=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, null=True, blank=True)

    phone_number = models.CharField(
        max_length=12, validators=[iran_phone_regex], unique=True, null=True, blank=True
    )
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Validate the model's attributes before saving.
        """
        # Validate that the table_number is not greater than the number of tables in the Cafe
        if self.table_number > self.cafe.number_of_tables:
            raise ValidationError(f"Table number cannot exceed {self.cafe.number_of_tables} for this cafe.")

    def save(self, *args, **kwargs):
        """
        Save the customer instance after validating its data.
        Calls the clean method to ensure data integrity before saving the instance.

        Args:
            *args, **kwargs: Additional arguments are passed to the superclass save method.
        """
        # Call clean method before saving
        # self.clean()
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        """Return the full name of the customer."""
        return f"{self.first_name} {self.last_name}"
