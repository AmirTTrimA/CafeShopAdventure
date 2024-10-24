# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Staff

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        try:
            user = Staff.objects.get(phone_number=phone_number)
        except Staff.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
