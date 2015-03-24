from django.forms import *
from django.contrib.auth.models import User

class SettingsForm(ModelForm):

    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'password']

