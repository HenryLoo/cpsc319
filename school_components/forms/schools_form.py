from django import forms
from school_components.models import School

class SchoolForm(forms.ModelForm):

	class Meta:
		model = School
		fields = '__all__'
		widgets = {
			'comments': forms.Textarea(attrs={'rows': 5}),
		}