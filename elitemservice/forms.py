from django import forms
from django.contrib.auth.forms import UserCreationForm

from elusermaneger.models import ElBaseUser


class LoginUser(forms.ModelForm):
    email = forms.EmailField(max_length=255, label="Email")
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="",)

    class Meta:
        model = ElBaseUser
        fields = ('email', 'password')


class RegisterUser(UserCreationForm):
    login = forms.CharField(max_length=255, label='Login')
    email = forms.EmailField(max_length=255, label='Email')
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="",)

    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="",)

    class Meta:
        model = ElBaseUser
        fields = ('login', 'email', 'password1', 'password2', )