# userAccount/models.py
from django.contrib.auth.models import User
from django.db import models
import random
<<<<<<< HEAD
=======
from proplistpage.models import Property
>>>>>>> Pei-Yi

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
<<<<<<< HEAD
=======
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    favorites = models.ManyToManyField(Property, related_name='favorited_by', blank=True)
>>>>>>> Pei-Yi

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        self.code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        self.save()