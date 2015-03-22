from django import forms
from django.forms import ModelForm, HiddenInput, DateInput
from school_components.models import Period, School

class PeriodForm(forms.ModelForm):

	school = forms.ModelChoiceField(queryset=School.objects.all(), required=True)

	class Meta:
		model = Period
		fields = '__all__'
		widgets = {
			'comments': forms.Textarea(attrs={'rows': 5}),
			'start_date': DateInput(attrs={'class':'datepicker'}),
			'end_date': DateInput(attrs={'class':'datepicker'}),
		}