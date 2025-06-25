from django.contrib import admin
from .models import UserProfile,EmailOTP
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(EmailOTP)
