from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.core.validators import MinLengthValidator



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        validators=[MinLengthValidator(3)],
    )
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['role', 'username', 'email', 'password1', 'password2']


class EditUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
