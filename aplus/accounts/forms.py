from django.forms import *
from django import forms
from accounts.models import Teachers, Users

class TeachersForm(ModelForm):

    email = forms.CharField(max_length=100, required=True, help_text="Email:" )
    name = forms.CharField(max_length=100, help_text="Name:" )
    phone = forms.CharField(max_length=15, help_text="Phone:" )
    skill_level = forms.CharField(max_length=2, help_text="Skill Level:" )

    class Meta():
        model = Teachers
        fields = ['email', 'name', 'phone', 'skill_level', 'description', 'status']
        widgets = {
 			'description' : forms.Textarea(attrs={'rows': '4', 'cols' : '42','maxlength' : Teachers._meta.get_field('description').max_length}),
        }

class TeachersAccount(ModelForm):

    class Meta():
        model = Users
        fields = ['email', 'password', 'role']
