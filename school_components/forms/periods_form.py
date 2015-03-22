from django import forms
from django.forms import ModelForm, HiddenInput, DateInput
from school_components.models import Period, School

class PeriodForm(forms.ModelForm):

	class Meta:
		model = Period
		school = forms.CharField(widget=forms.HiddenInput())
		fields = ['description','start_date', 'end_date', 'comments']
		widgets = {
			'comments': forms.Textarea(attrs={'rows': 5}),
			'start_date': DateInput(attrs={'class':'datepicker'}),
			'end_date': DateInput(attrs={'class':'datepicker'}),
		}