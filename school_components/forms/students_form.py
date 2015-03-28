from django import forms
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

class StudentFilter(forms.Form):
	name = forms.CharField(required=False)
	phone_number = forms.CharField(required=False)

StudentFormSet = forms.models.modelformset_factory(Student)