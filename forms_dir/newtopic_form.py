from django import forms
from boards.models import Topic
from mdeditor.fields import MDTextFormField

class NewTopic_Form(forms.ModelForm):
	message = MDTextFormField()
	class Meta:
		model = Topic
		fields = ['subject', 'message']
		help_texts = {'subject':'Maximum length is 300'}
		widgets = {'subject':forms.TextInput(attrs={'placeholder': 'enter subject of topic here'}) }	#model field subject is CharField so produces form field Charfield which has widget as TextInput
		#subject is of Topic and message(for Post ) declared outside Meta
