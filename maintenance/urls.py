
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_request, name='submit_request'),
    path('appointments/', views.view_appointments, name='view_appointments'),
    path('settings/', views.settings_view, name='maintenance_settings'),
]
