from django.db import models
from django.contrib.auth.models import User
from django import forms


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, required=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
