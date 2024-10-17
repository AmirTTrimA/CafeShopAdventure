"""
models.py

This module defines the Order and OrderItem models for the staff application,
including attributes related to customer orders and their items.
"""

from django.db import models
from staff.models import Staff
from customer.models import Customer
from menu.models import MenuItem


# class OrderItem(models.Model):
#     """
#     Model representing an item in an order.

#     Attributes:
#         order (ForeignKey): The order to which this item belongs.
#         item (ForeignKey): The menu item being ordered.
#         quantity (PositiveIntegerField): The quantity of the item ordered.
#         subtotal (DecimalField): The subtotal price for this item (calculated).
#         created_at (DateTimeField): The timestamp when the order item was created.
#         updated_at (DateTimeField): The timestamp when the order item was last updated.
#     """

#     order = models.ForeignKey(
#         Order, related_name="order_items", on_delete=models.CASCADE
#     )
#     item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         """Override save method to calculate subtotal before saving."""
#         self.subtotal = self.item.price * self.quantity
#         super(OrderItem, self).save(*args, **kwargs)

#     def __str__(self):
#         """Return a string representation of the order item."""
#         return f"{self.quantity} x {self.item.name} in Order {self.order.id}"


class Cart(models.Model):
    """
    Model representing a shopping cart for a customer.

    Attributes:
        customer (ForeignKey): The customer who owns the cart.
        created_at (DateTimeField): The timestamp when the cart was created.
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the cart."""
        return f"Cart for {self.customer.first_name} {self.customer.last_name}"


class CartItem(models.Model):
    """
    Model representing an item in a shopping cart.

    Attributes:
        cart (ForeignKey): The cart to which this item belongs.
        menu_item (ForeignKey): The menu item in the cart.
        quantity (PositiveIntegerField): The quantity of the menu item in the cart.
    """

    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """Return a string representation of the cart item."""
        return f"{self.quantity} x {self.menu_item.name} in Cart"

class Order(models.Model):
    """
    Model representing a customer order.

    Attributes:
        customer (ForeignKey): The customer who placed the order.
        staff (ForeignKey): The staff member handling the order (optional).
        order_date (DateTimeField): The date when the order was placed.
        status (CharField): The current status of the order.
        total_price (DecimalField): The total price of the order (calculated).
        created_at (DateTimeField): The timestamp when the order was created.
        updated_at (DateTimeField): The timestamp when the order was last updated.
    """

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
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
    cart_items = models.ManyToManyField(CartItem)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a string representation of the order."""
        return f"Order {self.id} by {self.customer.name}"

    def calculate_total_price(self):
        """Calculate the total price of the order based on its items."""
        total = sum(item.subtotal for item in self.order_items.all())
        self.total_price = total

    def save(self, *args, **kwargs):
        """Override save method to calculate total price before saving."""
        self.calculate_total_price()
        super(Order, self).save(*args, **kwargs)
