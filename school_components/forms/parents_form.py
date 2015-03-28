from django.forms import ModelForm, HiddenInput, DateInput, CharField, Form
from school_components.models import Parent, Payment
import django_filters

class ParentForm(ModelForm):
	class Meta:
		model = Parent
		exclude = ['school', 'period']


class PaymentForm(ModelForm):
	class Meta:
		model = Payment
		exclude = ['parent']
		# fields = ['receipt_no', 'amount', 'date']
		widgets = {
            'date': DateInput(attrs={'class':'datepicker'}),
        }

class ParentFilter(Form):
	name = CharField(required=False)
	receipt_no = CharField(required=False)