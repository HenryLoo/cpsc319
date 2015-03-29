from django import forms
from django.forms import ModelForm, HiddenInput, DateInput, ModelMultipleChoiceField, BooleanField
from school_components.models import Period, School, Department, Class, Course
from accounts.models import TeacherUser

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


class PeriodTransferForm(forms.Form):

        transfer_teachers = BooleanField(initial=True, required=False, label='Copy Teachers to New Period')

        def __init__(self, *args, **kwargs):
            super(PeriodTransferForm, self).__init__(*args)
            cur_school = kwargs.pop('cur_school')
            cur_period = kwargs.pop('cur_period')
            qs=Course.objects.filter(school=cur_school, period=cur_period)

            self.fields['courses'] = ModelMultipleChoiceField(queryset=qs, widget=forms.CheckboxSelectMultiple(), required=False, label='Copy Courses to New Period')
            
