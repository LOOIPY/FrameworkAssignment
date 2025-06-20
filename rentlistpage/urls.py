"""
URL configuration for rentlistpage app.
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'rentlistpage'

urlpatterns = [
    path('', views.rent_list, name='rent-list'),
    path('property/<int:property_id>/', views.rent_detail, name='rent-detail'),
]

# Add media static file support (only in DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)