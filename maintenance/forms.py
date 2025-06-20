from django import forms
from .models import MaintenanceRequest,Appointment

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'description', 'category', 'priority', 'requested_date', 'attachment']



class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'category', 'date', 'status']
