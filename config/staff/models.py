"""
models.py

This module defines the custom user model for the staff application,
extending the default Django user model to include additional fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.

    Attributes:
        phone_number (str): An optional phone number for the user.
    """

    phone_number = models.CharField(max_length=15, blank=True, null=True)
