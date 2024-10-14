from django.db import models
from config.staff.models import Staff
from config.order.models import Order  

class SalesAnalytics(models.Model):
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    total_orders = models.IntegerField(default=0, editable=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('date', 'staff')  

    def __str__(self):
        return f"Analytics for {self.staff} on {self.date}"

    def calculate_totals(self):
        orders = Order.objects.filter(order_date__date=self.date)
        self.total_orders = orders.count()
        total_sales_sum = 0
        for order in orders:
            total_sales_sum += order.total_price 
        self.total_sales = total_sales_sum

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super(SalesAnalytics, self).save(*args, **kwargs)
