# backends.py
from django.contrib.auth.backends import ModelBackend
from .models import Staff

class PhoneNumberBackend(ModelBackend):
    """
    Custom authentication backend that authenticates users based on their phone number.
    Attributes:
        model (Model): The model class to use for authentication, which should be a subclass of 
        Django's `User` model (in this case, `Staff`).
    """
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        """
        Authenticate a user based on the provided phone number and password.

        Args:
            request (HttpRequest): The HTTP request object.
            phone_number (str): The phone number of the user attempting to log in.
            password (str): The password of the user attempting to log in.
            **kwargs: Additional arguments that may be passed (unused in this method).

        Returns:
            User or None: If authentication is successful, returns the authenticated user
            instance. If authentication fails or the user does not exist, returns None.
        """
        try:
            user = Staff.objects.get(phone_number=phone_number)
        except Staff.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
