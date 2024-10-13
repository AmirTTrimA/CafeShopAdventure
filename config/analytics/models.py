"""
models.py

This module defines the Sales Analytics model for the staff application,
including attributes related to sales data.
"""

from django.db import models
from staff.models import Staff


class SalesAnalytics(models.Model):
    """
    Model representing sales analytics data.

    Attributes:
        analitics_id (int): The primary key for the sales analytics record (auto-incremented).
        date (datetime): The date of the sales analytics entry.
        total_sales (Decimal): The total sales amount for the given date.
        total_order (int): The total number of orders for the given date.
        staff_id (int): The ID of the staff member associated with the sales entry.
        create_at (datetime): The timestamp when the record was created.
        update_at (datetime): The timestamp when the record was last updated.
        relation_st_sl (ForeignKey): A relation to the Staff model, indicating which staff member handled the sales.
    """

    analitics_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()  # max_length is not applicable for DateTimeField
    total_sales = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Specify max_digits and decimal_places
    total_order = models.IntegerField()
    staff_id = models.ForeignKey(
        Staff, on_delete=models.CASCADE
    )  # Use ForeignKey instead of AutoField
    create_at = models.DateTimeField(
        auto_now_add=True
    )  # Automatically set the field to now when the object is created
    update_at = models.DateTimeField(
        auto_now=True
    )  # Automatically set the field to now every time the object is saved

    def __str__(self):
        """Return a string representation of the analytics record."""
        return f"{self.analitics_id}"
