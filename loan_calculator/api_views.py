from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal, ROUND_HALF_UP
from proplistpage.models import Property

@api_view(['POST'])
def calculate_loan_api(request):
    property_id = request.data.get('property_id')
    loan_percentage = Decimal(request.data.get('loan_percentage'))
    loan_years = Decimal(request.data.get('loan_years'))
    interest_rate = Decimal(request.data.get('interest_rate'))

    try:
        property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return Response({'error': 'Property not found'}, status=404)

    loan_amount = property.price * (loan_percentage / Decimal("100"))
    monthly_interest = (interest_rate / Decimal("100")) / Decimal("12")
    number_of_months = loan_years * Decimal("12")

    if monthly_interest > 0:
        monthly_payment = loan_amount * (monthly_interest * (1 + monthly_interest) ** number_of_months) / ((1 + monthly_interest) ** number_of_months - 1)
    else:
        monthly_payment = loan_amount / number_of_months

    total_payment = monthly_payment * number_of_months
    total_interest = total_payment - loan_amount

    result = {
        'property': property.title,
        'principal': str(loan_amount.quantize(Decimal('0.01'), ROUND_HALF_UP)),
        'interest': str(total_interest.quantize(Decimal('0.01'), ROUND_HALF_UP)),
        'monthly_payment': str(monthly_payment.quantize(Decimal('0.01'), ROUND_HALF_UP)),
    }

    return Response(result)
