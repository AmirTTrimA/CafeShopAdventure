"""forms.py"""
from django import forms
from django.contrib.auth.hashers import make_password
from .models import Staff

class OrderFilterForm(forms.Form):
    FILTER_CHOICES = [
        ('date', 'Date'),
        ('last_order', 'Last Order'),
        ('status', 'Status'),
        ('table_number', 'Table Number'),
    ]
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(label='Enter filter value',required=False)
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
        fields = ["phone_number", "first_name", "last_name", "password"]

    def save(self, commit=True):
        """Save the staff member, hashing the password before saving."""
        staff = super().save(commit=False)
        staff.password = self.cleaned_data["password"]
        if commit:
            staff.save()
        return staff
