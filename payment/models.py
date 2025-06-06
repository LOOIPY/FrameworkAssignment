# payment/models.py
from django.db import models
from loan_calculator.models import Property

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    status = models.CharField(max_length=20)


# Create your models here.
