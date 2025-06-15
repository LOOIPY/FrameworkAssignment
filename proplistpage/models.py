from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Property(models.Model):
    LOCATION_CHOICES = [
        ('KUALA LUMPUR', 'Kuala Lumpur'),
        ('SELANGOR', 'Selangor'),
        ('PENANG', 'Penang'),
        ('OTHERS', 'Others'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 🔥 Add this line
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    address = models.CharField(max_length=200, blank=True)
    detail = models.TextField(blank=True)
    image = models.ImageField(upload_to='property_images/')
    address = models.CharField(max_length=200, blank=True)  # 具体地址
    detail = models.TextField(blank=True)  # 房屋详情
    image = models.ImageField(upload_to='property_images/')
    #desmond part
    PROPERTY_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES, default='sale')
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.location}"


class PropertyImage(models.Model):

    property = models.ForeignKey(Property, related_name='extra_images', on_delete=models.CASCADE)
    image    = models.ImageField(upload_to='property_images/details/')
    caption  = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.property.title} - Image {self.id}"