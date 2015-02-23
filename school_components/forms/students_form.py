from django import forms
from school_components.models.parents_model import Parent
from school_components.models.students_model import Student

class StudentForm(forms.ModelForm):
	# first_name = forms.CharField(label='First Name', max_length=50)
	# last_name = forms.CharField(label='Last Name', max_length=50)
	# gender = forms.ChoiceField(label='Gender', choices=('M', 'F'))
	# birthdate = forms.DateField(label='Birthdate')
	# home_phone = forms.CharField(label='Home Phone', max_length=20)
	# address = forms.CharField(label='Address', max_length=75)
	# email = forms.EmailField(label='Email')
	# allergies = forms.CharField(label='Allergies', max_length=75)
	# emergency_contact_name = forms.CharField(label='Emergency Contact Name', max_length=75)
	# emergency_contact_phone = forms.CharField(label='Emergency Contact Phone', max_length=20)
	# parent = forms.ModelChoiceField(label='Parent', queryset=Parent.objects.all())
	# school = forms.ForeignKey('School')

	class Meta:
		model = Student
		fields = '__all__'

class StudentCSVForm(forms.Form):
	file = forms.FileField()


StudentFormSet = forms.models.modelformset_factory(Student)