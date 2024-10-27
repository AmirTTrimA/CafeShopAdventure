from django import forms

class CustomerSearchForm(forms.Form):
    phone_number = forms.CharField(max_length=12)
