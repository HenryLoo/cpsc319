from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Submit, Layout, HTML

class EMailForm(forms.Form):
    SEND_IND      = "-1"
    SEND_EVERYONE = "1"
    SEND_STUDENTS = "2"
    SEND_TEACHERS = "3"
    SEND_ADMINS   = "4"

    SEND_CHOICES = (
        (SEND_IND, ''),
        (SEND_EVERYONE, 'Everyone'),
        (SEND_STUDENTS, 'Students'),
        (SEND_TEACHERS, 'Teachers'),
        (SEND_ADMINS, 'Admins'),
    )

    to_group = forms.ChoiceField(label="To", choices=SEND_CHOICES, required=False)
    to_mail = forms.EmailField(label="Or ", error_messages={'required': "'To' field is required"}, required=False)
    subject_mail = forms.CharField(label="Subject", max_length=100, error_messages={'required': "'Subject' field is required"})
    content_mail = forms.CharField(label="Message", widget=forms.Textarea(attrs={'cols': 54, 'rows': 10}),
      error_messages={'required': "'Message' field is required"})

    def __init__(self, *args, **kwargs):
        super(EMailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form-email'
        self.helper.form_class = 'form-horizontal email-form'
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-8'

        self.helper.layout = Layout(
            Div(Field('to_group', css_class="select-md"),
                Field('to_mail', css_class="input-md"),
                css_class="row"),
            Div(HTML("<strong>&nbsp;</strong>")),
            Div(Field('subject_mail'), css_class="row"),
            Div(Field('content_mail'), css_class="row")
        )


    def clean(self):
        data = self.cleaned_data
        to_group = data.get('to_group', EMailForm.SEND_IND)
        to_ind = data.get('to_mail', '')

        if to_group == EMailForm.SEND_IND and len(to_ind) == 0 :
            raise forms.ValidationError('Please specify atleast one recipient')
        else:
            return data

