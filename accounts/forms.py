from django.forms import *
from django import forms
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm

#class TeachersForm(ModelForm):

 #   email = forms.CharField(max_length=100, required=True, help_text="Email:" )
  #  name = forms.CharField(max_length=100, help_text="Name:" )
   # phone = forms.CharField(max_length=15, help_text="Phone:" )
#    skill_level = forms.CharField(max_length=2, help_text="Skill Level:" )

 #   class Meta():
  #      model = Teachers
   #     fields = ['email', 'name', 'phone', 'skill_level', 'description', 'status']
    #    widgets = {
 #			'description' : forms.Textarea(attrs={'rows': '4', 'cols' : '42','maxlength' : Teachers._meta.get_field('description').max_length}),
  #      }

class MyUserCreationForm(UserCreationForm):

    email = EmailField(required=True)
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    
    def save(self, commit=True):
        user = super(MyUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class TeacherForm(ModelForm):

    class Meta():
        model = TeacherUser
        fields = ['phone', 'branch_location', 'skill_level']

class AdminForm(ModelForm):

    admin_type = forms.ChoiceField(choices=( ('SYSTEM_ADMIN', "System Admin"), ('SCHOOL_ADMIN', "School Admin") ))
    class Meta():
        model = AdminUser
        fields = ['phone', 'branch_location']


class AvailabilityForm(ModelForm):
    
    class Meta():
        model = TeachingAvailability
        fields = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        
    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(self, *args, **kwargs)
        self.fields['monday'].initial  = True
        self.fields['tuesday'].initial  = True
        self.fields['wednesday'].initial  = True
        self.fields['thursday'].initial  = True
        self.fields['friday'].initial  = True
            
    

