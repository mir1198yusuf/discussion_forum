from django import forms
from boards.models import Post
from mdeditor.fields import MDTextFormField

class TopicReply_Form(forms.ModelForm):
	message = MDTextFormField()
	class Meta:
		model = Post
		fields = ['message']
		
		
	