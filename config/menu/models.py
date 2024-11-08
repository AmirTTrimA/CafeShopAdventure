"""
models.py

This module defines the Category and MenuItem models for the menu application,
including attributes related to menu items and their categories.
"""

from django.db import models


class Category(models.Model):
    """
    Model representing a category of menu items.

    Attributes:
        name (str): The name of the category.
        created_at (datetime): The timestamp when the category was created.
        updated_at (datetime): The timestamp when the category was last updated.
    """

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the name of the category."""
        return f"{self.name}"


class MenuItem(models.Model):
    """
    Model representing a menu item.

    Attributes:
        name (str): The name of the menu item.
        description (str): A description of the menu item (optional).
        price (Decimal): The price of the menu item.
        points (int): Reward points associated with the menu item.
        category (ForeignKey): The category to which this menu item belongs.
        is_available (bool): Availability status of the menu item.
        created_at (datetime): The timestamp when the menu item was created.
        updated_at (datetime): The timestamp when the menu item was last updated.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    points = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)  # multichoice status
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the name of the menu item."""
        return f"{self.name}"
