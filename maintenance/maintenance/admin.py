
from django.contrib import admin
from .models import MaintenanceRequest, Appointment, MaintenanceCategory, MaintenanceSettings

admin.site.register(MaintenanceRequest)
admin.site.register(Appointment)
admin.site.register(MaintenanceCategory)
admin.site.register(MaintenanceSettings)
