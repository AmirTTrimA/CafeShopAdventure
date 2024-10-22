"""
models.py

This module defines the Order and OrderItem models for the staff application,
including attributes related to customer orders and their items.
"""

from django.db import models
from staff.models import Staff
from customer.models import Customer
from menu.models import MenuItem


class Order(models.Model):
    """
    Represents a customer order in the system.

    Attributes:
        customer (Customer): The customer associated with the order.
        staff (Staff): The staff member handling the order.
        order_date (DateTimeField): The date and time when the order was placed.
        status (str): The current status of the order (Pending, Completed, Canceled).
        total_price (Decimal): The total price of the order, calculated automatically.
        created_at (DateTimeField): The timestamp when the order was created.
        updated_at (DateTimeField): The timestamp when the order was last updated.
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Canceled", "Canceled"),
        ],
        default="Pending",
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the Order.

        Returns:
            str: A string indicating the order ID and customer phone number or 'Guest'.
        """
        return f"Order {self.id} by {self.customer.phone_number if self.customer else 'Guest'}"

    def calculate_total_price(self):
        total = sum(item.subtotal for item in self.order_items.all())
        self.total_price = total

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate the total price before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # First save the Order instance to the database
        super().save(*args, **kwargs)

        # Now that the Order is saved, you can access the order_items
        self.calculate_total_price()


class OrderItem(models.Model):
    """
    Represents an item within an order.

    Attributes:
        order (Order): The order to which this item belongs.
        item (MenuItem): The menu item being ordered.
        quantity (int): The quantity of the menu item ordered.
        subtotal (Decimal): The subtotal price for this item, calculated automatically.
        created_at (DateTimeField): The timestamp when the item was created.
        updated_at (DateTimeField): The timestamp when the item was last updated.
    """

    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate the subtotal before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """

        self.subtotal = (
            self.item.price * self.quantity
        )  # Assuming item has a price attribute
        super().save(*args, **kwargs)
        if self.order:
            self.order.calculate_total_price()
            self.order.save()

    def __str__(self):
        """
        Returns a string representation of the OrderItem.

        Returns:
            str: A string indicating the quantity and item name in the corresponding order.
        """
        return f"{self.quantity} x {self.item.name} in Order {self.order.id}"


class OrderHistory(models.Model):
    """
    Model to store order history in JSON format.

    Attributes:
        customer (Customer): The customer associated with the order history.
        guest_id (str): An identifier for guest users.
        order_data (JSONField): Stores the order details in JSON format.
        created_at (DateTimeField): The timestamp when the order history was created.
    """

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True
    )
    guest_id = models.CharField(
        max_length=36, null=True, blank=True
    )  # For guest tracking
    order_data = models.JSONField()  # Stores the order details in JSON format
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the OrderHistory.

        Returns:
            str: A string indicating the customer phone number and creation date.
        """
        return f"Order by {self.customer.phone_number} on {self.created_at}"
