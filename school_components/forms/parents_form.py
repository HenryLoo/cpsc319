from django.forms import ModelForm, HiddenInput
from school_components.models import Parent, Payment

class ParentForm(ModelForm):
	class Meta:
		model = Parent
		exclude = ['school', 'period']


class PaymentForm(ModelForm):
	class Meta:
		model = Payment
		fields = ['receipt_no', 'amount', 'date']