# from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import userInfo
from django.forms import ModelForm


# Create your forms here.

class loginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)

class send_reset_Form(forms.Form):
	email = forms.EmailField(required=True)

class change_pass_Form(forms.Form):
	password1 = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)	
	password2 = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput)

class registerForm(ModelForm):
	password = forms.CharField(max_length=200, widget=forms.PasswordInput)
	password_confirm = forms.CharField(max_length=200, widget=forms.PasswordInput)
	class Meta:
		model = userInfo
		fields = ('username', 'email', 'password', 'password_confirm')

