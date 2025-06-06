from django.urls import path
from . import views

urlpatterns = [
    path('credit-card-payment/<int:property_id>', views.credit_card_payment, name='credit_card_payment'),
    path('booking-list/', views.booking_list, name='booking_list'),
    path('online-banking/<str:bank_name>/<int:property_id>', views.online_banking_login, name='online_banking_login'),
    path('fpx-confirmation/<str:bank_name>/<int:property_id>', views.fpx_confirmation, name='fpx_confirmation'),
    path('e-wallet-payment/<int:property_id>/<str:wallet_name>/', views.e_wallet_payment, name='e_wallet_payment'),

]
