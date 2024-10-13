from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class StaffManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Staff must have an email address')
        email = self.normalize_email(email)
        staff = self.model(email=email, first_name=first_name, last_name=last_name)
        staff.set_password(password)  
        staff.save(using=self._db)
        return staff

    def create_superuser(self, email, first_name, last_name, password=None):
        staff = self.create_user(email, first_name, last_name, password)
        staff.is_admin = True
        staff.is_superuser = True
        staff.save(using=self._db)
        return staff
    
class Staff(models.Model,AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('manager', 'manager'),
        ('waiter', 'waiter'),
        ('chef', 'chef'),
        ('assistant cook', 'assistant cook'),
        ('dish washer','dish washer'),
        ('services','services')


    )
    staff_id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=40,choices=ROLE_CHOICES)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    # relation_st_or=models.ForeignKey(Order,on_delete=models.CASCADE)

    objects = StaffManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self):
        return self.is_superuser


