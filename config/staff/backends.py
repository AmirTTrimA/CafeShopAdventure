from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(phone_number=phone_number)
            if user:
                print(f"Found user: {user}")
        except UserModel.DoesNotExist:
            print("User not found")
            return None

        if user.check_password(password):
            print("Password is correct")
            return user
        print("Password is incorrect")
        return None
