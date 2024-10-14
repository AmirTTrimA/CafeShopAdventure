"""
models.py

This module defines the Staff model and its manager for the application,
including attributes related to staff members and their roles.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class StaffManager(BaseUserManager):
    """
    Custom manager for the Staff model.

    Methods:
        create_user: Creates and returns a regular user with an email and password.
        create_superuser: Creates and returns a superuser with admin privileges.
    """

    def create_user(self, email, first_name, last_name, password=None):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError("Staff must have an email address")
        email = self.normalize_email(email)
        staff = self.model(email=email, first_name=first_name, last_name=last_name)
        staff.set_password(password)
        staff.save(using=self._db)
        return staff

    def create_superuser(self, email, first_name, last_name, password=None):
        """Create and return a superuser with admin privileges."""
        staff = self.create_user(email, first_name, last_name, password)
        staff.is_admin = True
        staff.is_superuser = True
        staff.save(using=self._db)
        return staff


class Staff(AbstractBaseUser, PermissionsMixin, models.Model):
    """
    Model representing a staff member.

    Attributes:
        ROLE_CHOICES (tuple): Available roles for staff members.
        staff_id (int): Unique identifier for the staff member.
        first_name (str): The first name of the staff member.
        last_name (str): The last name of the staff member.
        email (str): The email address of the staff member (unique).
        role (str): The role of the staff member.
        create_at (datetime): The timestamp when the staff member was created.
        update_at (datetime): The timestamp when the staff member was last updated.
    """

    ROLE_CHOICES = (
        ("manager", "manager"),
        ("waiter", "waiter"),
        ("chef", "chef"),
        ("assistant cook", "assistant cook"),
        ("dish washer", "dish washer"),
        ("services", "services"),
    )

    # staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=40, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=True)  
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = StaffManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",'email']

    def __str__(self):
        """Return the full name of the staff member."""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        """Check if the staff member is an admin."""
        return self.is_superuser
