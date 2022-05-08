from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                       'placeholder': 'Логин'}))
    email = forms.CharField(label='', widget=forms.EmailInput(attrs={'class': 'form_input',
                                                                     'placeholder': 'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form_input',
                                                                            'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form_input',
                                                                            'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form_input',
                                                                       'placeholder': 'Логин'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form_input',
                                                                           'placeholder': 'Пароль'}))


class VINForm(forms.Form):
    vin = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'your_vin', 'placeholder': 'Укажите VIN'}))


class RecoveryPassForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'txtb', 'placeholder': 'Логин'}))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'txtb', 'placeholder': 'Почта'}))


class CreateNewPassword(UserCreationForm):
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'txtb',
                                                                            'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'txtb',
                                                                            'placeholder': 'Подтвердите пароль'}))