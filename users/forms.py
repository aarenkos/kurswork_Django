from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class PasswordAltResetForm(forms.Form):
    email = forms.EmailField(
        label="Укажите вашу электронную почту",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )