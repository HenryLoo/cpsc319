from django.forms import ModelForm, HiddenInput, DateInput
from school_components.models import Parent, Payment

class ParentForm(ModelForm):
	class Meta:
		model = Parent
		# exclude = ['school', 'period']


class PaymentForm(ModelForm):
	class Meta:
		model = Payment
		exclude = ['parent']
		# fields = ['receipt_no', 'amount', 'date']
		widgets = {
            'date': DateInput(attrs={'class':'datepicker'}),
        }