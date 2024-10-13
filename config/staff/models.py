from django.db import models



class Staff(models.Model):
    ROLE_CHOICES = (
        ('Manager', 'Manager'),
        ('Waiter', 'Waiter'),
        ('Chef', 'Chef'),
        ('assistant cook', 'assistant cook'),
        ('dish washer','dish washer'),
        ('Services','Services')


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


