from django.forms import *
from django import forms
from school_components.models import *
from accounts.models import TeacherUser
from django.forms.models import BaseModelFormSet

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


class ClassRegistrationForm(Form):
	class Meta:
		model = ClassRegistration
		fields = ['student']
		widgets = {
			'student': forms.TextInput(
				attrs={
					'id': 'search-student-input',
					'class': 'form-control',
					'type': 'text',
					'placeholder': 'Search for student...'
				}
			),
		}

class RemoveClassRegistrationForm(Form):
	student_id = forms.CharField(widget=forms.HiddenInput())


class ClassAssignmentForm(ModelForm):
	content  = forms.FileField()

	class Meta:
		model = Assignment
		fields = ['title', 'date', 'grade_weight', 'total_weight', 'comments']
		widgets = {
			'comments': forms.Textarea(attrs={'rows': 5}),
			'date': DateInput(attrs={'class':'datepicker'}),
		}

class ClassGradingForm(ModelForm):

	student = forms.ModelChoiceField(queryset=Student.objects.all(),required=False)
	reg_class = forms.ModelChoiceField(queryset=Class.objects.all(), required=False)
	class Meta:
		model = Grading
		fields = ['student', 'grade', 'comments', 'reg_class']

class ClassAttendanceForm(ModelForm):
    attendance = ChoiceField(label='', choices=(('A', 'A'), ('P', 'P'), ('L', 'L')), required=False)
    
    class Meta:
        model = ClassAttendance
        fields = ['comments', 'attendance']
