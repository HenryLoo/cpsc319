from django import forms
from school_components.models import School

class SchoolForm(forms.ModelForm):

	class Meta:
		model = School
		fields = ['title', 'address', 'phone']
