from django import forms
from django.contrib.auth.models import User

class MyProfileUpdate_Form(forms.ModelForm):
	#redefining these fields because these fields are blank=True in User model
	#alternate way is to define widget inside Meta class and there pass html attrs
	email = forms.EmailField(max_length=254, required=True)
	first_name = forms.CharField(max_length=30, required=True)
	last_name = forms.CharField(max_length=150, required=True)
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']