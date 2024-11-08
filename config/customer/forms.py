from django import forms

class CustomerSearchForm(forms.Form):
    """
    Searches for a customer based on the provided search form.
    """
    phone_number = forms.CharField(max_length=12)
