
from django.shortcuts import render, redirect
from .forms import MaintenanceRequestForm
from .models import MaintenanceRequest, Appointment, MaintenanceSettings

def submit_request(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.created_by = request.user
            maintenance_request.save()
            return redirect('view_appointments')
    else:
        form = MaintenanceRequestForm()
    return render(request, 'maintenance/submit_request.html', {'form': form})

def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'maintenance/view_appointments.html', {'appointments': appointments})

def settings_view(request):
    settings = MaintenanceSettings.objects.first()
    return render(request, 'maintenance/settings.html', {'settings': settings})
