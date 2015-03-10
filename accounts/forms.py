from django.forms import *
from django import forms
from django.forms import models
from accounts.models import *

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext as _

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

#class MyUserCreationForm(UserCreationForm):

#    email = EmailField(required=True)
#    first_name = CharField(required=True)
#    last_name = CharField(required=True)
#    
#    def save(self, commit=True):
#        user = super(MyUserCreationForm, self).save(commit=False)
#        user.email = self.cleaned_data["email"]
#        user.first_name = self.cleaned_data["first_name"]
#        user.last_name = self.cleaned_data["last_name"]
#        if commit:
#            user.save()
#        return user

class UserCreationForm(ModelForm):

    error_messages = {
        'duplicate_email': _("A user with that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
  
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'address', 'school_branch']

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class TeacherForm(UserCreationForm):

    skill_level = IntegerField(required=False)
    monday = BooleanField(initial=True)
    tuesday = BooleanField(initial=True)
    wednesday = BooleanField(initial=True)
    thursday = BooleanField(initial=True)
    friday = BooleanField(initial=True)
    comments = CharField(widget=forms.Textarea)
    
    def save(self, commit=True):
        user = super(TeacherForm, self).save(commit=False) #there might be an error here since role is required. might be able to fix  by unrequiring it and deafult to TEA
        user.role = 'TEA'
        
        teacherinfo = TeacherInfo(skill_level = self.cleaned_data['skill_level'])
        teacherinfo.user_info = user

        avail = TeachingAvailability()
        avail.monday = self.cleaned_data['monday']
        avail.tuesday = self.cleaned_data['tuesday']
        avail.wednesday = self.cleaned_data['wednesday']
        avail.thursday = self.cleaned_data['thursday']
        avail.friday = self.cleaned_data['friday']
        avail.comments = self.cleaned_data['comments']
        teacherinfo.teaching_availability = avail
        
        if commit:
            user.save()
            avail.save()
            teacherinfo.save()
            
        return teacherinfo

class AdminForm(UserCreationForm):

    admin_type = forms.ChoiceField(choices=( ('SYS', "System Admin"), ('SCH', "School Admin") ), required=True)

    def save(self, commit=True):
        user = super(AdminForm, self).save(commit=False)
        user.role = self.cleaned_data['admin_type']
        
        if commit:
            user.save()
            
        return user

#class AvailabilityForm(ModelForm):
    
#    class Meta():
#        model = TeachingAvailability
#        fields = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        
   
class LoginForm(forms.Form):

    email = EmailField(max_length=100, required=True)
    password = CharField(max_length=100, required=True)

    

