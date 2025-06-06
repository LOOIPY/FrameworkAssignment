from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('checklist/', views.checklist, name='checklist'),
    path('invoice/', views.invoice, name='invoice'),
    path('', views.home, name='home'),
]
