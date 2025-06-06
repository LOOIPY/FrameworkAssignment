from django.shortcuts import render
from django.views.generic import ListView
from .models import GameReview

# Create your views here.
class GameReviewListView(ListView):
    model = GameReview
    template_name = 'gamereview_list.html'
    context_object_name = 'reviews'
    ordering = ['-date_posted']  # 按发布日期降序排列
