from django import forms
from school_components.models import Class

class ParentContactRegistrationForm(forms.Form):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	cell_phone = forms.CharField(max_length=20)
	email = forms.EmailField()
	parent_comments = forms.CharField(max_length=500)

	emergency_first_name = forms.CharField(max_length=75)
	emergency_last_name = forms.CharField(max_length=75)
	emergency_contact_phone = forms.CharField(max_length=20)
	contact_comments = forms.CharField(max_length=500)


class StudentRegistrationForm(forms.Form):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	gender = forms.MultipleChoiceField(
							widget=forms.RadioSelect,
							choices=(('MALE', 'M'),
									('FEMALE', 'F')))
	birthdate = forms.DateField()
	home_phone = forms.CharField(max_length=20)
	address = forms.CharField(max_length=75)
	email = forms.EmailField()
	allergies = forms.CharField(max_length=75)
	comments = forms.CharField(max_length=500)

	# create fields for all the classes offered this school/period
	def __init__(self, *args, **kwargs):
		school = kwargs.pop('school_id')
		period = kwargs.pop('period_id')

		super(StudentRegistrationForm, self).__init__(*args, **kwargs)

		classes = Class.objects.filter(
			school = school, period = period
		)

		choices = {}

		# create dict of depts and their class sections
		# ie. {'Math': [('M101', 'Math Level 1'), ('M201', Math Level 2')]}
		for classs in classes:
			dept = 'dept' + classs.course.department.name
			if dept not in choices:
				choices[dept] = []			
			choices[dept].append((classs.id, 
				'%s %s' % (classs.course.name, classs.section)))
		
		for dept, sections in choices.iteritems():
			self.fields[dept] = forms.ChoiceField(choices=sections)


class PaymentRegistrationForm(forms.Form):
	receipt_no = forms.CharField(max_length=50)
	amount = forms.DecimalField(max_digits=10, decimal_places=2)
	date = forms.DateField()


class SummaryRegistrationForm(forms.Form):
	a = forms.CharField(max_length=50)

