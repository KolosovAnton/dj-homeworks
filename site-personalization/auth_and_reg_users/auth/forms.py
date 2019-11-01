from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя:', widget=forms.TextInput)
    password1 = forms.CharField(label='Придумайте пароль:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль:', widget=forms.PasswordInput)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя:', widget=forms.TextInput)
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput)
