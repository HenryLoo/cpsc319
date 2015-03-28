from django import forms
import django_filters
from school_components.models.students_model import Student

class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		exclude = ['school', 'period']
		widgets = {
            'birthdate': forms.DateInput(attrs={'class':'datepicker'}),
        }

class StudentCSVForm(forms.Form):
	file = forms.FileField()

class StudentFilter(django_filters.FilterSet):
	class Meta:
		model = Student
		fields = {
			'first_name': ['icontains'],
			'last_name': ['icontains'], 
			'home_phone': ['icontains'],
		}




StudentFormSet = forms.models.modelformset_factory(Student)