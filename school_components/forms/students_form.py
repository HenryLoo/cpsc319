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

class StudentViewForm(forms.Form):
	view = forms.ChoiceField(
					label="View Students:",
					widget=forms.RadioSelect(),
					choices=(('all', 'All'),
							('period', 'Enrolled in Period')))

StudentFormSet = forms.models.modelformset_factory(Student)