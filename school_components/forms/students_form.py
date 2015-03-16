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


StudentFormSet = forms.models.modelformset_factory(Student)