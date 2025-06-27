"""
URL configuration for proplistpage app.
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'proplistpage'

urlpatterns = [
    path('', views.property_list, name='property-list'),
    path('property/<int:pk>/', views.property_detail, name='property-detail'),
    path('new-launches/', views.new_launches_view, name='new-launches'),
]

# Add media static file support (only in DEBUG mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)