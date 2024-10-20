"""staff/forms.py"""

from django import forms
from django.contrib.auth.hashers import make_password
from .models import Staff
from .validator import iran_phone_regex


class StaffRegistrationForm(forms.ModelForm):
    """
    A form for registering new staff members.
    """

    phone_number = forms.CharField(
        validators=[iran_phone_regex],
        help_text="Enter a valid Iranian phone number (e.g., +989123456789 or 09123456789)",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Password",
        help_text="Enter a strong password with at least 8 characters",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm Password",
        help_text="Enter the same password as above, for verification",
    )

    class Meta:
        """
        Meta class to configure the StaffRegistrationForm.

        Attributes:
            model (Staff): The model associated with this form.
            fields (list): The fields to include in the form.
        """

        model = Staff
        fields = ["phone_number", "password1", "password2", "role"]

    # def clean_phone_number(self):
    #     """Validate and format the phone number."""
    #     phone_number = self.cleaned_data.get("phone_number")
    #     # Remove any non-digit characters
    #     phone_number = "".join(filter(str.isdigit, phone_number))
    #     if phone_number.startswith("0"):
    #         phone_number = "+98" + phone_number[1:]
    #     elif not phone_number.startswith("+98"):
    #         phone_number = "+98" + phone_number
    #     return phone_number

    def clean(self):
        """
        Validate that the two password fields match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match.")
            if len(password1) < 8:
                raise forms.ValidationError(
                    "Password must be at least 8 characters long."
                )

        return cleaned_data

    def save(self, commit=True):
        """Save the staff member, setting the password."""
        staff = super().save(commit=False)
        staff.password = self.cleaned_data["password1"]
        if commit:
            staff.save()
        return staff
