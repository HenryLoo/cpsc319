from django import forms
from school_components.models.students_model import Student
from school_components.models.classes_model import *
class ClassForm(forms.ModelForm):
	class Meta:
		model = Class
		fields = ['course', 'section', 'description', 'class_size', 'waiting_list_size', 'room']


class ClassScheduleForm(forms.ModelForm):
	class Meta:
		model = ClassSchedule
		exclude = ['sch_class']
		widgets = {
			'start_time': forms.TimeInput(
				attrs={
					'class':'form-inline',
					'type': 'time',
				}),
			'end_time': forms.TimeInput(
				attrs={
					'class':'form-inline',
					'type': 'time',
				}),
		}

class ClassTeacherForm(forms.ModelForm):
	class Meta:
		model = ClassTeacher
		fields = ['teacher']

class ClassRegistrationForm(forms.ModelForm):
	student = forms.ModelChoiceField(
        queryset=Student.objects.all(),                       
        widget=forms.CheckboxSelectMultiple, 
        empty_label=None,
        required=False
    )

	class Meta:
		model = ClassRegistration
		fields = ['student']



