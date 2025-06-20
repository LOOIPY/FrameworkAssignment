from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name='dashboard'

urlpatterns = [
    path('checklist/', views.checklist, name='checklist'),
    path('invoice/', views.invoice, name='invoice'),
]
