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
from .validator import iran_phone_regex


class StaffManager(BaseUserManager):
    """
    Custom manager for the Staff model.

    Methods:
        create_user: Creates and returns a regular user with a phone number and password.
        create_superuser: Creates and returns a superuser with admin privileges.
    """

    def create_user(self, phone_number, password=None):
        """Create and return a regular user with a phone number and password."""
        if not phone_number:
            raise ValueError("The phone number field must be set")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.role = "S"
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        """Create and return a superuser with admin privileges."""
        user = self.create_user(phone_number, password)
        user.role = "M"
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
        phone_number (str): The phone number of the staff member (unique).
        role (str): The role of the staff member.
        create_at (datetime): The timestamp when the staff member was created.
        update_at (datetime): The timestamp when the staff member was last updated.
        password (str): The hashed password of the staff member.
        is_active (bool): Status indicating if the staff member account is active.
        is_superuser (bool): Status indicating if the staff member is a superuser.
    """

    ROLE_CHOICES = (
        ("M", "Manager"),
        ("S", "Staff"),
    )

    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=12, validators=[iran_phone_regex], unique=True
    )
    role = models.CharField(max_length=1, choices=ROLE_CHOICES)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    @property
    def is_staff(self):
        """Check if the staff member has admin privileges."""
        return self.role == "M"

    objects = StaffManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Return the full name of the staff member."""
        return f"{self.first_name} {self.last_name}"

    def check_password(self, raw_password):
        """Check the provided password against the stored hashed password."""
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        """Override save method to set is_superuser based on role and hash password."""
        self.is_superuser = (self.role == 'M')
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        """Set the password and mark it as changed."""
        self.password = raw_password
        self._password_changed = True