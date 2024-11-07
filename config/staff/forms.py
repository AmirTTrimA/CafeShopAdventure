"""staff/forms.py"""

from django import forms
from .models import Staff


class OrderFilterForm(forms.Form):
    """
    A form for filtering orders based on various criteria.

    Attributes:
        FILTER_CHOICES (list): A list of choices for filtering types,
                                including date, last order, status, and table number.
        filter_type (ChoiceField): A field to select the type of filter.
        filter_value (CharField): A field to input the value to filter by.
    """

    FILTER_CHOICES = [
        ("date", "Date"),
        ("last_order", "Last Order"),
        ("status", "Status"),
        ("table_number", "Table Number"),
        ("my_orders", "my orders"),
        ("all", "all"),
    ]
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(label="Enter filter value", required=False)


class OrderFilterFormManager(forms.Form):
    """
    A form for filtering orders based on various criteria.

    Attributes:
        FILTER_CHOICES (list): A list of choices for filtering types,
                                including date, last order, status, and table number.
        filter_type (ChoiceField): A field to select the type of filter.
        filter_value (CharField): A field to input the value to filter by.
    """

    FILTER_CHOICES = [
        ("staff_null", "staff_null"),
        ("date", "Date"),
        ("last_order", "Last Order"),
        ("status", "Status"),
        ("table_number", "Table Number"),
        ("my_orders", "my orders"),
        ("all", "all"),
    ]
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(label="Enter filter value", required=False)


class StaffRegistrationForm(forms.ModelForm):
    """
    A form for registering new staff members.
    """

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter your last name"})
    )

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter a valid Iranian phone number (e.g., +989123456789 or 09123456789"
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter a strong password with at least 8 characters"}
        ),
        label="Confirm Password",
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter the same password as above, for verification"}
        ),
        label="Confirm Password",
    )

    class Meta:
        """
        Meta class to configure the StaffRegistrationForm.

        Attributes:
            model (Staff): The model associated with this form.
            fields (list): The fields to include in the form.
        """

        model = Staff
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "password1",
            "password2",
            "role",
        ]

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


class DataAnalysisForm(forms.Form):
    """
    A form for selecting the type of data analysis to perform.

    Attributes:
        FILTER_CHOICES (list): A list of choices for data analysis types,
                                including popular items and peak business hours.
        filter_type (ChoiceField): A field to select the type of analysis filter.
    """

    FILTER_CHOICES = [
        ("most popular caffe items", "popular items"),
        ("peak business hour", "peak hour"),
        # tested but not active because of the reasons by Mr.Kashi
        # ("customer demographic data",'demographic data'),
    ]
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES)


class SaleAnalysisForm(forms.Form):
    """
    A form for selecting the type of sales analysis to perform.

    Attributes:
        FILTER_CHOICES (list): A list of choices for sales analysis types,
                                including total, daily, monthly, and yearly sales.
        filter_type (ChoiceField): A field to select the type of sales analysis filter.
    """

    FILTER_CHOICES = [
        ("total sales", "total sales"),
        ("daily sales", "daily sales"),
        ("monthly sales", "monthly sales"),
        ("yearly sales", "yearly sales"),
    ]
    filter_type = forms.ChoiceField(choices=FILTER_CHOICES)
