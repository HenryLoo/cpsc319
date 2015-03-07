from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from messages.forms import EMailForm
import sendgrid

def send_email(request):
    if request.method == 'POST':

        form = EMailForm(request.POST)
        if form.is_valid():
            to_mail = str(form.cleaned_data['to_mail'])
            subject_mail = str(form.cleaned_data['subject_mail'])
            content_mail = str(form.cleaned_data['content_mail'])

            sg = sendgrid.SendGridClient(settings.sashaseifollahi, settings.cpsc31911)

            message = sendgrid.Mail()
            message.add_to(to_mail)
            message.set_subject(subject_mail)
            message.set_html(content_mail)
            message.set_text(content_mail)
            message.set_from('sashaseifollahi@gmail.com')
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
    