from django import forms

class SampleLogin_Form(forms.Form):
	name = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		fields = ['name','password']