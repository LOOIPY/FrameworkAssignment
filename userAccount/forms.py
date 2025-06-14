from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
<<<<<<< HEAD
=======
from proplistpage.models import Property
>>>>>>> c036076 (login,signup,profile,my property,and for the rent i added urls file cause initially i get error for it, but the rent list and rent details design seems not completely prepared. And i have changed some design for the homepage css)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number']
<<<<<<< HEAD
=======

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'location', 'price', 'image', 'address', 'detail', 'type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }
>>>>>>> c036076 (login,signup,profile,my property,and for the rent i added urls file cause initially i get error for it, but the rent list and rent details design seems not completely prepared. And i have changed some design for the homepage css)
