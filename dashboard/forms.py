from django import forms
from dashboard.models import Chart, NotificationType

class ChartForm(forms.ModelForm):
	class Meta:
		model = Chart
		exclude = ['school', 'period']

class NotificationsSettingsForm(forms.ModelForm):
	condition = forms.IntegerField(widget=forms.NumberInput(attrs={'style': 'width:45px; height:32px'}), label='')
	content = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:550px; height:32px'}), label='')
	class Meta:
		model = NotificationType
		exclude = ['notification_type']