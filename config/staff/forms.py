"""forms.py"""
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
        fields = ["phone_number", "first_name", "last_name", "password"]

    def save(self, commit=True):
        """Save the staff member, hashing the password before saving."""
        staff = super().save(commit=False)
        staff.password = self.cleaned_data["password"]
        if commit:
            staff.save()
        return staff

class FilterOrderForm(forms.Form):
    FILTER_CHOICES = [
        ('date', 'Filter by Date'),
        ('table', 'Filter by Table Number'),
        ('last_order', 'View Last Order'),
        ('status', 'Filter by Status'),
    ]
    STATUS_FILD=[('Done','done'),('paide','paide')]
    
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES)
    
    # These fields will appear based on the selected filter type
    date = forms.DateField(required=False)
    table_number = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=STATUS_FILD, required=False)
