from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Booking
from proplistpage.models import Property
from payment.utils import calculate_payment
from django.urls import reverse
import qrcode
import base64
from io import BytesIO
from django.contrib.auth.decorators import login_required

@login_required
def credit_card_payment(request, property_id):
    property = Property.objects.get(id=property_id)
    payment_info = calculate_payment(property)  # use the utility
    amount = payment_info['amount']

    if request.method == "POST":
        card_number = request.POST.get("card_number", "").strip()
        expiry = request.POST.get("expiry", "").strip()
        name = request.POST.get("name", "").strip()
        cvv = request.POST.get("cvv", "").strip()

        print(f"card_number={card_number}, expiry={expiry}, name={name}, cvv={cvv}")

        if not card_number or not expiry or not name or not cvv:
            return render(request, 'payment/credit_card_payment.html', {
                'property': property,
                'amount': amount,
                'error': "Please fill in all fields."
            })

        # Example validation: 16 digits card number, 3 digit CVV
        if not (card_number.isdigit() and len(card_number) == 16 and cvv.isdigit() and len(cvv) == 3):
            return render(request, 'payment/credit_card_payment.html', {
                'property': property,
                'amount': amount,
                'error': "Invalid card number or CVV."
            })

        Booking.objects.create(
            property=property,
            total_payment=amount,
            date=timezone.now(),
            status='Paid'
        )
        property.is_booked = True
        property.save()
        return render(request, 'payment/loading.html', {'redirect_url': 'booking_list'})

    return render(request, 'payment/credit_card_payment.html', {'property': property, 'amount': amount})

@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'payment/booking_list.html', {'bookings': bookings})


@login_required
def online_banking_login(request, bank_name, property_id):
    if request.method == 'POST':
        return redirect('fpx_confirmation', bank_name=bank_name, property_id=property_id)

    return render(request, 'payment/online_banking_login.html', {
        'bank_name': bank_name.capitalize(),
        'property_id': property_id
    })

@login_required
def fpx_confirmation(request, bank_name, property_id):
    try:
        property_obj = Property.objects.get(id=property_id)
        payment_info = calculate_payment(property_obj)
        amount = payment_info['amount']
    except Property.DoesNotExist:
        property_obj = None
        amount = 0

    if request.method == 'POST' and property_obj:
        Booking.objects.create(
            property=property_obj,
            total_payment=amount,
            date=timezone.now(),
            status='Paid'
        )
        property_obj.is_booked = True
        property_obj.save()
        return render(request, 'payment/loading.html', {'redirect_url': 'booking_list'})

    return render(request, 'payment/fpx_confirmation.html', {
        'bank_name': bank_name.capitalize(),
        'amount': amount,
        'property_id': property_id
    })

@login_required
def e_wallet_payment(request, property_id, wallet_name):
    try:
        property_obj = Property.objects.get(id=property_id)
        payment_info = calculate_payment(property_obj)
        amount = payment_info['amount']
    except Property.DoesNotExist:
        property_obj = None
        amount = 0

    # Generate QR Code (random value)
    qr = qrcode.make(f"PAY {amount} to {wallet_name}")
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()

    if request.method == 'POST' and property_obj:
        Booking.objects.create(
            property=property_obj,
            total_payment=amount,
            date=timezone.now(),
            status='Paid'
        )
        property_obj.is_booked = True
        property_obj.save()
        return render(request, 'payment/loading.html', {'redirect_url': 'booking_list'})

    return render(request, 'payment/e_wallet_payment.html', {
        'wallet_name': wallet_name.capitalize(),
        'amount': amount,
        'qr_code_base64': qr_code_base64,
        'property_id': property_id
    })

# Create your views here.
