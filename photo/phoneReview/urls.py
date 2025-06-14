from django.urls import path
from . import views

app_name = 'phoneReview'

urlpatterns = [
    path('', views.index, name='index'),
]