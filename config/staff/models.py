"""
models.py

This module defines the Staff model and its manager for the application,
including attributes related to staff members and their roles.
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
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
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """Create and return a superuser with admin privileges."""
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


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
        password (str): The hashed password of the staff member.
        is_active (bool): Status indicating if the staff member account is active.
        is_staff (bool): Status indicating if the staff member has staff privileges.
    """

    ROLE_CHOICES = (
        ("manager", "Manager"),
        ("waiter", "Waiter"),
        ("chef", "Chef"),
        ("assistant cook", "Assistant Cook"),
        ("dish washer", "Dish Washer"),
        ("services", "Services"),
    )

    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=40, choices=ROLE_CHOICES)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StaffManager()

    def save(self, *args, **kwargs):
        """Override save method to hash the password before saving."""
        if self.pk is None and self.password:  # Only hash if creating a new user
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        """Return the full name of the staff member."""
        return f"{self.first_name} {self.last_name}"

    def check_password(self, raw_password):
        """Check the provided password against the stored hashed password."""
        return check_password(raw_password, self.password)
