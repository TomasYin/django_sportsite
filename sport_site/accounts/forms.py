from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserProfile


class SignUpForm(UserCreationForm):
	email = forms.CharField(
		max_length=254,
		required=False,
		widget=forms.EmailInput())
	class Meta():
		model = User
		fields = ('username','email','password1','password2')

class UserProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	class Meta:
		model = UserProfile
		fields = ('picture',)
	
		