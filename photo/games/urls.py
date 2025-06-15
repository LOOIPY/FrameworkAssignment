from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('reviews/', views.GameReviewListView.as_view(), name='review-list'),
]