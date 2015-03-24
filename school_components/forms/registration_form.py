from django import forms
from school_components.models import Class, Payment

class ParentContactRegistrationForm(forms.Form):
	first_name = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'placeholder': "First name",
				'type':'text'
			}
		))
	last_name = forms.CharField(max_length=50, 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'placeholder': "Last name",
				'type': 'text'
			}))
	cell_phone = forms.CharField(max_length=20,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type': "tel"
			}))
	email = forms.EmailField(
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type': "email"
			}))
	parent_comments = forms.CharField(
		max_length=500,
		required=False,
		widget=forms.Textarea(
			attrs= {
				'class': 'form-control',
				'rows': 2
			}
		))

	emergency_first_name = forms.CharField(
		max_length=75,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type':'text',
				'placeholder': "First name"
			}
		))
	emergency_last_name = forms.CharField(
		max_length=30,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type':'text',
				'placeholder': "Last name"
			}
		))
	emergency_relation = forms.CharField(
		max_length=45,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type':'text'
			}
		))
	emergency_cell_phone = forms.CharField(
		max_length=20,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type': 'tel'
			}
		))
	emergency_home_phone = forms.CharField(
		max_length=20,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type': 'tel'
			}
		))
	contact_comments = forms.CharField(
		max_length=500,
		required=False,
		widget=forms.Textarea(
			attrs={
				'class': 'form-control',
				'rows': 2
			}
		))


class StudentRegistrationForm(forms.Form):
	first_name = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'placeholder': "First name",
				'type':'text'
			}
		))
	last_name = forms.CharField(
		max_length=50, 
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'placeholder': "Last name",
				'type':'text'
			}
		))
	gender = forms.ChoiceField(
				widget=forms.RadioSelect,
				choices=(('MALE', 'M'),
						('FEMALE', 'F')))
	birthdate = forms.DateField(
		widget=forms.DateInput(
			attrs={'class':'datepicker form-control'}
		))

	home_phone = forms.CharField(
		max_length=20,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type':'tel'
			}
		))
	address = forms.CharField(
		max_length=75,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'placeholder': "Street address, City, Postal Code",
				'type':'text'
			}
		))
	email = forms.EmailField(
		required=False,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type':'email'
			}
		))
	allergies = forms.CharField(
		max_length=75,
		required=False,
		widget=forms.TextInput(
			attrs={
				'class': 'form-control', 
				'type':'text'
			}
		))
	comments = forms.CharField(
		max_length=500,
		required=False,
		widget=forms.Textarea(
			attrs={
				'class': 'form-control', 
				'rows': 3
			}
		))

	# create fields for all the classes offered this school/period
	def __init__(self, *args, **kwargs):
		school = kwargs.pop('school_id')
		period = kwargs.pop('period_id')

		super(StudentRegistrationForm, self).__init__(*args, **kwargs)

		classes = Class.objects.filter(
			school = school, period = period
		)

		choices = {}

		# create dict of depts and their class sections for UI
		# ie. {'Math': [('M101', 'Math Level 1'), ('M201', Math Level 2')]}
		for classs in classes:
			dept = classs.course.department.name
			if dept not in choices:
				choices[dept] = [('', '----')]			
			choices[dept].append(
				('id_%d' % classs.id, 
				'%s %s %s' % (classs.course.name, classs.section, classs.schedule)))
		
		for dept, sections in choices.iteritems():
			self.fields[dept] = forms.ChoiceField(
				choices=sections, 
				help_text='dept',
				required=False,
				widget=forms.Select(
					attrs={ 'class': 'form-control class-dropdown' }
				)
			)


class PaymentRegistrationForm(forms.ModelForm):
	receipt_no = forms.CharField(max_length=50,
		widget=forms.TextInput(
			attrs={
				'class':'form-control',
				'type': 'text'
			}
		))
	amount = forms.DecimalField(max_digits=10, decimal_places=2,
		widget=forms.TextInput(
			attrs={
				'class':'form-control'
			}
		))
	date = forms.DateField(
		widget=forms.DateInput(
			attrs={
				'class':'datepicker form-control'
			}
		))
	class Meta:
		model = Payment
		exclude = ['parent']


class SummaryRegistrationForm(forms.Form):
	a = forms.CharField(widget=forms.HiddenInput())

