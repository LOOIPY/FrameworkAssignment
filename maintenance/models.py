
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MaintenanceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



# Model to store Maintenance Requests
class MaintenanceRequest(models.Model):
    CATEGORY_CHOICES = [
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
        ('HVAC', 'HVAC'),
        ('General Maintenance', 'General Maintenance'),
    ]

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    requested_date = models.DateField()
    attachment = models.FileField(upload_to='maintenance_attachments/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Only use auto_now_add

    def __str__(self):
        return self.title

class MaintenanceSettings(models.Model):
    notify_by_email = models.BooleanField(default=True)
    default_priority = models.CharField(max_length=50, default='Medium')


class Appointment(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


