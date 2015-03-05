from django import forms
from messages.models import Email

class EmailForm(forms.Form):
	email = forms.EmailField()
	subject = forms.CharField(max_length=100)
	attach = forms.Field(widget = forms.FileInput, required=False)
	message = forms.CharField(widget = forms.Textarea)