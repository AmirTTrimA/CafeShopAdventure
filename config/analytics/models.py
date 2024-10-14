from django.db import models
from staff.models import Staff
from order.models import Order


class SalesAnalytics(models.Model):
    """
    Model to track sales analytics for staff members.

    Attributes:
        date (DateField): The date for the sales analytics.
        total_sales (DecimalField): Total sales amount for the date.
        total_orders (IntegerField): Total number of orders for the date.
        staff (ForeignKey): Reference to the staff member associated with the analytics.
        created_at (DateTimeField): Timestamp when the record was created.
        updated_at (DateTimeField): Timestamp when the record was last updated.
    """

    date = models.DateField()
    total_sales = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, editable=False
    )
    total_orders = models.IntegerField(default=0, editable=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("date", "staff")
        verbose_name_plural = "Sales Analytics"

    def __str__(self):
        """Return a string representation of the sales analytics record."""
        return f"Analytics for {self.staff} on {self.date}"

    def calculate_totals(self):
        """
        Calculate total orders and total sales for the given date.

        This method fetches all orders for the specified date and calculates
        the total number of orders and the total sales amount.
        """
        orders = Order.objects.filter(order_date__date=self.date)
        self.total_orders = orders.count()
        self.total_sales = sum(order.total_price for order in orders)

    def save(self, *args, **kwargs):
        """
        Override the save method to calculate totals before saving.

        This method ensures that total orders and total sales are calculated
        each time the record is saved.
        """
        self.calculate_totals()
        super(SalesAnalytics, self).save(*args, **kwargs)
