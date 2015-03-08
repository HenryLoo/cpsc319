from django import forms
from school_components.models.students_model import Student
from school_components.models.classes_model import Class, ClassRegistration

class ClassForm(forms.ModelForm):
	class Meta:
		model = Class
		fields = '__all__'

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
