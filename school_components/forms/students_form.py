from django import forms
from school_components.models import Student

class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'

class StudentCSVForm(forms.Form):
	file = forms.FileField()
