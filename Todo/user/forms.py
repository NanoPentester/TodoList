from email.policy import default

from django import forms
from django.contrib.auth.models import  User


class RegsiterForm(forms.Form):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    email = forms.EmailField(label='enter your email')
    password = forms.CharField(widget=forms.PasswordInput)


class ForgetPassForm(forms.Form):
    email = forms.EmailField(label='enter your email')


class VerifyOtpForm(forms.Form):
    otp = forms.CharField(max_length=255 ,label='press the otp')


class ResetPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput , label='enter the password')
    confirmPassword = forms.CharField(widget=forms.PasswordInput , label='confirm the password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email']


class PasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']