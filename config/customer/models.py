from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

class Customer(models.Model):
    iran_phone_regex = RegexValidator(
        regex=r'^(\+98|0)?9\d{9}$',  
        message="Phone number must be entered in the format: '+989xxxxxxxxx' or '09xxxxxxxxx'."
    )
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, validators=[iran_phone_regex]) 
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  
        super(Customer, self).save(*args, **kwargs)
