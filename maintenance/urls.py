from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('submit/', views.submit_request, name='submit_request'),
    path('appointments/', views.view_appointments, name='view_appointments'),
    path('settings/', views.settings_view, name='maintenance_settings'),
    path('requests/', views.view_requests, name='view_requests'),
     path('add/', views.add_appointment, name='add_appointment'),
    path('view/', views.view_appointments, name='view_appointments'),
]

