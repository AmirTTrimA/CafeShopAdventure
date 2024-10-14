from django import forms
from django.contrib.auth.hashers import make_password
from .models import Staff


class StaffRegistrationForm(forms.ModelForm):
    """
    A form for registering new staff members.

    Attributes:
        password (CharField): The password field for the staff member.
    """

    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        """
        Meta class to configure the StaffRegistrationForm.

        Attributes:
            model (Staff): The model associated with this form.
            fields (list): The fields to include in the form.
        """

        model = Staff
        fields = ["email", "first_name", "last_name", "password"]

    def save(self, commit=True):
        """Save the staff member, hashing the password before saving."""
        staff = super().save(commit=False)
        staff.password = make_password(
            self.cleaned_data["password"]
        )  # Hash the password
        if commit:
            staff.save()
        return staff
