from django.db import models

class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='sale')
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name
