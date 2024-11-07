from django.core.validators import RegexValidator

iran_phone_regex = RegexValidator(
    regex=r"^(\+98|0)?9\d{9}$",
    message="Phone number must be entered in the format: '+989xxxxxxxxx' or '09xxxxxxxxx'.",
)
