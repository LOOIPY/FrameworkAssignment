# userAccount/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()

@receiver(user_logged_in)
def ensure_profile_exists(sender, request, user, **kwargs):
    UserProfile.objects.get_or_create(user=user)
