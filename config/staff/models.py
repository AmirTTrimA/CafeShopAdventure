from django.db import models

class Staff(models.Model):
    staff_id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=40)
    role = models.CharField(max_length=40)
    create_at = models.DateTimeField(max_length=40)
    update_at = models.DateTimeField(max_length=40)
    # relation_st_or=models.ForeignKey(Order,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
