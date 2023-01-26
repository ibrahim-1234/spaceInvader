# from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import userInfo
from django.forms import ModelForm


# Create your forms here.

class loginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(max_length=25, required=True, widget=forms.PasswordInput)

class registerForm(ModelForm):
	password = forms.CharField(max_length=25, widget=forms.PasswordInput)
	password_confirm = forms.CharField(max_length=25, widget=forms.PasswordInput)
	class Meta:
		model = userInfo
		fields = ('username', 'email', 'password', 'password_confirm')

