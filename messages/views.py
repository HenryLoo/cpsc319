from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
import sendgrid
from school_components.models.students_model import *
from messages.forms import EMailForm

def clear_messages(request):
        storage = get_messages(request)
        for message in storage:
            print message

def send_email(request):
    clear_messages(request)
    if request.method == 'POST':
        form = EMailForm(request.POST)
        if form.is_valid():
            to_group = str(form.cleaned_data['to_group'])
            to_mail = str(form.cleaned_data['to_mail'])
            subject_mail = str(form.cleaned_data['subject_mail'])
            content_mail = str(form.cleaned_data['content_mail'])

            sg = sendgrid.SendGridClient(settings.SENDGRID_EMAIL_USERNAME, settings.SENDGRID_EMAIL_PASSWORD)

            message = sendgrid.Mail()

            if to_group != EMailForm.SEND_IND:
                #fetching recipients
                email_lists = None
                if to_group == EMailForm.SEND_STUDENTS:
                    #TODO Add additional filters here
                    email_lists = Student.objects.all().values_list('email', flat=True)
                elif to_group == EMailForm.SEND_TEACHERS:
                    print "TODO"
                elif to_group == EMailForm.SEND_ADMINS:
                    print "TODO"
                elif to_group == EMailForm.SEND_EVERYONE:
                    print "TODO"

                if email_lists:
                    message.add_bcc(email_lists)
            else:
                message.add_to(to_mail)

            message.set_subject(subject_mail)
            message.set_html(content_mail)
            message.set_text(content_mail)
            message.set_from('sashaseifollahi@gmail.com') #TODO logged in user here
            status, msg = sg.send(message)

            if status == 200:
                messages.success(request, 'Your email was successfully sent.')
            else:
                messages.error(request, msg)
    else:
        form = EMailForm()

    return render(request, 'messages/messages_page.html', {
        'form': form,
    })

def sent_mail(request):
    return render(request, 'messages/sent_mail.html')
    