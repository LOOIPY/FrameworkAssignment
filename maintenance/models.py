
from django.db import models
from django.contrib.auth.models import User

class MaintenanceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MaintenanceRequest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(MaintenanceCategory, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=50)
    requested_date = models.DateField()
    attachment = models.FileField(upload_to='maintenance/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending')

class Appointment(models.Model):
    request = models.ForeignKey(MaintenanceRequest, on_delete=models.CASCADE)
    staff_assigned = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=50)

class MaintenanceSettings(models.Model):
    notify_by_email = models.BooleanField(default=True)
    default_priority = models.CharField(max_length=50, default='Medium')
