from django.shortcuts import render, get_object_or_404
from proplistpage.models import Property
from payment.utils import calculate_payment
from loan_calculator.forms import LoanCalculatorForm
from decimal import Decimal, ROUND_HALF_UP

def home(request):
    for_sale = Property.objects.filter(type='sale', is_booked=False)
    for_rent = Property.objects.filter(type='rent', is_booked=False)
    return render(request, 'main/home.html', {
        'for_sale': for_sale,
        'for_rent': for_rent
    })

def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    payment_info = calculate_payment(property)

    # Always initialize the form (no POST handling needed)
    form = LoanCalculatorForm(initial={'property': property})

    # No more result calculation here; frontend will fetch it from API
    result = None

    return render(request, 'main/property_detail.html', {
        'property': property,
        'payment_info': payment_info,
        'form': form,
        'result': result
    })

