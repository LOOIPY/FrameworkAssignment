from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:property_id>/', views.property_detail, name='property_detail'),
]
