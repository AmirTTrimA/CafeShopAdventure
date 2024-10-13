from django.db import models
from config.staff.models import Staff
from config.customer.models import Customer
from config.menu.models import MenuItem
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE,null=True,blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

    def calculate_total_price(self):
        total = sum(item.subtotal for item in self.order_items.all())
        self.total_price = total

    def save(self, *args, **kwargs):
        self.calculate_total_price()
        super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.subtotal = self.item.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Order {self.order.id}"