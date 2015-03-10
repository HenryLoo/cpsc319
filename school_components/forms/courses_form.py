from django import forms
from school_components.models import Course, Prerequisite, Department 

class CourseForm(forms.ModelForm):
	prerequisite = forms.ModelChoiceField(queryset=Course.objects.all(), 
		required=False)

	class Meta:
		model = Course
		fields = ['name', 'department', 'prerequisite', 
				'age_requirement', 'description']
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
		}


class PrerequisiteForm(forms.ModelForm):
	class Meta:
		model = Prerequisite
		fields = '__all__'


class DepartmentForm(forms.ModelForm):
	class Meta:
		model = Department
		fields = '__all__'
		widgets = {
			'description': forms.Textarea(attrs={'rows': 5}),
		}