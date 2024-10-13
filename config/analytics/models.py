from django.db import models
from staff.models import Staff

class Sales_Analytics(models.Model):
    analitics_id=models.AutoField(primary_key=True)
    date=models.DateTimeField()
    total_sales=models.DecimalField(max_digits=10, decimal_places=2)
    total_order=models.IntegerField()
    staff_id = models.ForeignKey(
        Staff, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # relation_st_sl=models.ForeignKey(Staff,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.analitics_id}"
