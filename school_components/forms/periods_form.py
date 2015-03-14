from django import forms
from school_components.models import Period, School

class PeriodForm(forms.ModelForm):

	school = forms.ModelChoiceField(queryset=School.objects.all(), required=False)

	class Meta:
		model = Period
		fields = '__all__'
