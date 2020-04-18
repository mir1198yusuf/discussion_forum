from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User 

class SignUp_Form(UserCreationForm):
	#usercreationform doesnot have email field but user model has
	email = forms.EmailField(max_length=254, required=True)	
	#email in user model has maxlength 254 obtained from  print(User._meta.get_field('email').max_length)
	#to get all attribute values use User._meta.get_field('email').__dict__
	class Meta:
		model = User
		fields = ['username','email','password1','password2']