"""
models.py

This module defines the Staff model for the staff application,
including attributes for staff members.
"""

from django.db import models


class Staff(models.Model):
    """
    Model representing a staff member.

    Attributes:
        staff_id (int): The primary key for the staff member (auto-incremented).
        first_name (str): The first name of the staff member.
        last_name (str): The last name of the staff member.
        email (str): The unique email address of the staff member.
        password (str): The password of the staff member (should be hashed).
        role (str): The role of the staff member.
        create_at (datetime): The timestamp when the staff member was created.
        update_at (datetime): The timestamp when the staff member was last updated.
    """

    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(
        max_length=128
    )  # Password should be hashed; max length should be at least 128 chars
    role = models.CharField(
        max_length=40
    )  # For roles, create a class and use choices in Django
    create_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set the field to now when the object is created
    update_at = models.DateTimeField(
        auto_now=True
    )  # Automatically set the field to now every time the object is saved

    def __str__(self):
        """Return a string representation of the staff member."""
        return f"{self.first_name} {self.last_name}"
