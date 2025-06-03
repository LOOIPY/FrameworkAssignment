# payment/utils.py
from decimal import Decimal
def calculate_payment(property_obj):
    if property_obj.type == 'rent':
        return {
            'label': 'Total Payment',
            'amount': property_obj.cost,
        }
    elif property_obj.type == 'sale':
        deposit = property_obj.cost * Decimal('0.02')
        return {
            'label': 'Earnest Deposit (2%)',
            'amount': deposit,
        }
    else:
        return {
            'label': 'N/A',
            'amount': 0,
        }
