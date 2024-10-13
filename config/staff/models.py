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

class Staff(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Waiter', 'Waiter'),
        ('Chef', 'Chef'),
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)  
    is_staff = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StaffManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self):
        return self.is_superuser
