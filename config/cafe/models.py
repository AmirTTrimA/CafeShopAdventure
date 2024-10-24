from django.db import models
from django.contrib.auth.models import User
from config import settings
class Cafe(models.Model):
    """
    Represents a Cafe in the system.

    Attributes:
        name (str): The name of the cafe.
        address (str): The address of the cafe.
        owner (ForeignKey): The owner (User) of the cafe.
        opening_time (TimeField): The time the cafe opens.
        closing_time (TimeField): The time the cafe closes.
      
    """
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    opening_time = models.TimeField()  
    closing_time = models.TimeField()  
    created_at = models.TimeField()

    def __str__(self):
        return f"{self.name} owned by {self.owner.username}"

    def is_open(self, current_time):
        """
        Check if the cafe is open based on the current time.
        """
        return self.opening_time <= current_time <= self.closing_time
