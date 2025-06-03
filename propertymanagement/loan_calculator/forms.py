from django import forms
from .models import Property

class LoanCalculatorForm(forms.Form):
    property = forms.ModelChoiceField(
        queryset=Property.objects.filter(type='sale'),
        label='Property (For Sale Only)'
    )
    loan_percentage = forms.DecimalField(min_value=0, max_value=100)
    loan_years = forms.IntegerField(min_value=1, max_value=35)
    interest_rate = forms.DecimalField(min_value=0, max_digits=5, decimal_places=2)
