from django.forms import *
from django import forms
from accounts.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

# class MyUserCreationForm(UserCreationForm):
    # email = EmailField(required=True)
    # first_name = CharField(required=True)
    # last_name = CharField(required=True)
    

    # def save(self, commit=True):
    #     user = super(MyUserCreationForm, self).save(commit=False)
    #     user.username = self.cleaned_data["email"]
    #     user.email = self.cleaned_data["email"]

    #     #password = generate random password, check if unique
    #     #user.password = password
    #     user.first_name = self.cleaned_data["first_name"]
    #     user.last_name = self.cleaned_data["last_name"]
    #     if commit:
    #         user.save()
    #     return user
class MyUserCreationForm(ModelForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta():
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']


#WILL NOT USE THIS IF WE'RE JUST STORING THE PASSWORD DIRECTLY IN THE DB
class MyUserEditForm(ModelForm):

    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta():
        model = User
        fields = ['email', 'first_name', 'last_name'] #no password changing on edit


#This is for restricting school admins to being able to only create school admins
class NoRoleAdminProfileForm(ModelForm):
    
    class Meta():
        model = UserProfile
        fields = ['phone']
        
class AdminProfileForm(ModelForm):

    role = ChoiceField(label='Admin Type', choices=(('SYSTEM_ADMIN', 'System Admin'), ('SCHOOL_ADMIN', 'School Admin')), required=True)
    
    class Meta():
        model = UserProfile
        fields = ['phone', 'role']

class TeacherProfileForm(ModelForm):
    
    class Meta():
        model = UserProfile
        fields = ['phone']

class TeacherForm(ModelForm):
    
    comments = forms.CharField(max_length = 500, widget=forms.Textarea, required=False)
    
    class Meta():
        model = TeacherUser
        fields = ['comments']


class TeacherCSVForm(forms.Form):
	file = forms.FileField()
	
class AvailabilityForm(ModelForm):
    
    class Meta():
        model = TeachingAvailability
        fields = '__all__'
        
   

class LoginForm(forms.Form):

    email = EmailField(max_length=100, required=True)
    password = CharField(max_length=100, required=True)

    

