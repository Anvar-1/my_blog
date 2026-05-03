from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Parolni tiklash uchun haqiqiy email kiriting.")

    class Meta:
        model = User
        fields = ['username', 'email']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'avatar', 'cover_image', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        }