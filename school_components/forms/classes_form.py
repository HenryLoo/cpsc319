from django.forms import *
from django import forms
from school_components.models import *
from accounts.models import TeacherUser

class ClassForm(ModelForm):
	class Meta:
		model = Class
		fields = ['course', 'section', 'description', 'class_size', 'waiting_list_size', 'room']


class ClassScheduleForm(ModelForm):
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

class ClassTeacherForm(ModelForm):
	class Meta:
		model = ClassTeacher
		fields = ['teacher']


class ClassRegistrationForm(ModelForm):
	student = forms.ModelChoiceField(
        queryset=Student.objects.all(),                       
        widget=forms.CheckboxSelectMultiple, 
        empty_label=None,
        required=False
    )

	class Meta:
		model = ClassRegistration
		fields = ['student']

class ClassAttendanceForm(ModelForm):
    attendance = ChoiceField(label='', choices=(('A', 'A'), ('P', 'P'), ('L', 'L')), required=False)
    
    class Meta:
        model = ClassAttendance
        fields = ['comments', 'attendance']


class ClassAssignmentForm(ModelForm):
	content  = forms.FileField()

	class Meta:
		model = Assignment
		fields = ['title', 'date', 'grade_weight', 'total_weight', 'comments']
		widgets = {
			'comments': forms.Textarea(attrs={'rows': 5}),
			'date': DateInput(attrs={'class':'datepicker'}),
		}
