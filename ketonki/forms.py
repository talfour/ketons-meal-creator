from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form__input','placeholder': 'Wpisz swój login'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form__input', 'placeholder':'Podaj hasło'}))


class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True, widget=EmailInput(attrs={'class':'form__input','placeholder':'Adres e-mail'}))
	username = forms.CharField(required=True, widget=TextInput(attrs={'class':'form__input','placeholder':'Nazwa użytkownika'}))
	password1 = forms.CharField(widget=PasswordInput(attrs={'class':'form__input','placeholder':'Hasło'}))
	password2 = forms.CharField(widget=PasswordInput(attrs={'class':'form__input','placeholder':'Powtórz hasło'}))
	captcha = CaptchaField()
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Nazwa użytkownika'
		self.fields['password2'].label= 'Powtórz hasło'

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		
		if commit:
			user.save()
		return user