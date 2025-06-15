from django.contrib import admin
from .models import Phone, Review

# Register your models here.
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'release_date')
    search_fields = ('name', 'brand')
    list_filter = ('brand', 'release_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('phone', 'reviewer_name', 'rating', 'date_posted')
    list_filter = ('rating', 'date_posted')
    search_fields = ('reviewer_name', 'comment')
