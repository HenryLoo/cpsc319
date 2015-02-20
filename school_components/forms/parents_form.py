from django.forms import ModelForm
from school_components.models import Parent

class ParentForm(ModelForm):
	class Meta:
		model = Parent
		fields = '__all__'