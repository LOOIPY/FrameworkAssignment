from django.contrib import admin
from .models import Game, GameReview

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'developer', 'release_date', 'genre')
    search_fields = ('name', 'developer')
    list_filter = ('genre', 'release_date')

@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'reviewer_name', 'rating', 'date_posted')
    list_filter = ('rating', 'date_posted')
    search_fields = ('reviewer_name', 'comment')
