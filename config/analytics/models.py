from django.db import models
from config.staff.models import Staff

class SalesAnalytics(models.Model):
    date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    total_orders = models.IntegerField(default=0)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('date', 'staff') 

    def __str__(self):
        return f"Analytics for {self.staff} on {self.date}"
