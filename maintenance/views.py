from django.shortcuts import render, redirect
from .models import MaintenanceRequest, Appointment, MaintenanceSettings
from .forms import MaintenanceRequestForm,AppointmentForm

# View to handle Maintenance Request submission
def submit_request(request):
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.created_by = request.user
            maintenance_request.save()
            return redirect('maintenance:view_requests')  # Redirect to view requests after submission
    else:
        form = MaintenanceRequestForm()
    return render(request, 'maintenance/submit_request.html', {'form': form})

# View to display all submitted maintenance requests
def view_requests(request):
    requests = MaintenanceRequest.objects.all().order_by('-created_at')
    return render(request, 'maintenance/view_requests.html', {'requests': requests})

# View Appointments View
def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'maintenance/view_appointments.html', {'appointments': appointments})

# Settings View (Admin)
def settings_view(request):
    settings = MaintenanceSettings.objects.first()  # Assuming there's only one settings record
    return render(request, 'maintenance/settings.html', {'settings': settings})



# View to show the form to add an appointment
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Assuming you have a user field on the Appointment model
            appointment.save()
            return redirect('maintenance:view_appointments')  # Redirect to the view appointments page
    else:
        form = AppointmentForm()

    return render(request, 'maintenance/add_appointments.html', {'form': form})

# View to show all appointments of the logged-in user
def view_appointments(request):
    appointments = Appointment.objects.filter(user=request.user)  # Assuming user is a foreign key in Appointment model
    return render(request, 'maintenance/view_appointments.html', {'appointments': appointments})

