from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    #path('', views.loan_calculator, name='loan_calculator'),
    path('api/calculate-loan/', api_views.calculate_loan_api, name='calculate_loan_api'),
]