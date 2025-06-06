from django.contrib import admin
from .models import Property

admin.site.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'type']
    list_filter = ['type']
# Register your models here.
