from django.db import models

from staff.models import Staff

class Sales_Analytics(models.Model):
    analitics_id=models.AutoField(primary_key=True)
    date=models.DateTimeField(max_length=40)
    total_sales=models.DecimalField()
    total_order=models.IntegerField()
    staff_id=models.AutoField()
    create_at = models.DateTimeField(max_length=40)
    update_at = models.DateTimeField(max_length=40)
    relation_st_sl=models.ForeignKey(Staff,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.analitics_id}"
