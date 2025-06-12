from django.shortcuts import render, get_object_or_404
from .forms import LoanCalculatorForm
from proplistpage.models import Property
from decimal import Decimal, ROUND_HALF_UP

def loan_calculator(request):
    result = None
    initial_data = {}

    #  If a property_id is passed in URL, pre-select that property
    property_id = request.GET.get('property_id')
    if property_id:
        try:
            initial_data['property'] = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            pass  # Do nothing if invalid ID

    if request.method == 'POST':
        form = LoanCalculatorForm(request.POST)
        if form.is_valid():
            property = form.cleaned_data['property']
            loan_percentage = Decimal(form.cleaned_data['loan_percentage'])
            loan_years = Decimal(form.cleaned_data['loan_years'])
            interest_rate = Decimal(form.cleaned_data['interest_rate'])

            # Calculations using Decimal
            loan_amount = property.cost * (loan_percentage / Decimal("100"))
            monthly_interest = (interest_rate / Decimal("100")) / Decimal("12")
            number_of_months = loan_years * Decimal("12")

            if monthly_interest > 0:
                monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest) ** number_of_months) / ((1 + monthly_interest) ** number_of_months - 1)
            else:
                monthly_payment = loan_amount / number_of_months

            total_payment = monthly_payment * number_of_months
            total_interest = total_payment - loan_amount

            result = {
                'property': property.name,
                'principal': loan_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'interest': total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
                'monthly_payment': monthly_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            }
    else:
        form = LoanCalculatorForm(initial=initial_data)  # ✅ Pass initial data only on GET

    return render(request, 'loan_calculator/calculator.html', {'form': form, 'result': result})
