from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sendgrid
from school_components.models import *
from accounts.models import UserProfile, TeacherUser
from .models import SentMessage
from aplusmessages.forms import EMailForm

def clear_messages(request):
        storage = get_messages(request)
        for message in storage:
            print message



'''
Stores email in database
'''
def save_email(request, to_type, to_emails, cc_emails, bcc_emails, from_email, subject, body, html_body, status, status_message):
    return SentMessage.objects.create(recipient_type=to_type, to_list=to_emails, cc_list=cc_emails, bcc_list=bcc_emails,
                                      from_email=from_email, subject=subject, body=body, html_body=html_body,
                                      status=status, status_message=status_message)



def get_send_choices(request):
    user_choices = SentMessage.SEND_CHOICES
    
    '''
    for dep in Department.objects.all():
        dep = (dep.name, "DEP-"+str(dep.id),)
        user_choices = user_choices + (dep,)
    '''
    return user_choices



'''
sends email to selected group of people or to individual
'''
def send_email(request):
    clear_messages(request)
    if request.method == 'POST':
        form = EMailForm(request.POST, choices=get_send_choices(request))
        if form.is_valid():
            to_group = str(form.cleaned_data['to_group'])
            to_mail = str(form.cleaned_data['to_mail'])
            subject_mail = str(form.cleaned_data['subject_mail'])
            content_mail = str(form.cleaned_data['content_mail'])

            sg = sendgrid.SendGridClient(settings.SENDGRID_EMAIL_USERNAME, settings.SENDGRID_EMAIL_PASSWORD)

            message = sendgrid.Mail()

            '''
            # if an individual is not specified and group is selected
            '''
            if to_group != SentMessage.SEND_IND:
                #fetching recipients
                email_lists = None
                if to_group == SentMessage.SEND_STUDENTS:
                    '''
                    students are selected
                    '''
                    #TODO Add additional filters here if required e.g. students belongs to logged in user
                    email_lists = Student.objects.all().values_list('email', flat=True)
                elif to_group == SentMessage.SEND_TEACHERS:
                    '''
                    teachers are selected
                    '''
                    #TODO Add additional filters here if required  e.g. teachers belongs to logged in user
                    email_lists = TeacherUser.objects.all().values_list('user__user__email', flat=True)
                elif to_group == SentMessage.SEND_ADMINS:
                    '''
                    admins are selected
                    '''
                    #TODO Add additional filters here if required  e.g. admins belongs to logged in user
                    email_lists =  UserProfile.objects.filter(role__in=UserProfile.ADMIN_ROLES).values_list('user__email', flat=True)
                elif to_group == SentMessage.SEND_EVERYONE:
                    #TODO Add additional filters here if required
                    email_lists = []

                    for semail in Student.objects.all().values_list('email', flat=True):
                        email_lists.append(semail)

                    for temail in TeacherUser.objects.all().values_list('user__user__email', flat=True):
                        email_lists.append(temail)

                    for aemail in UserProfile.objects.filter(role__in=UserProfile.ADMIN_ROLES).values_list('user__email', flat=True):
                        email_lists.append(aemail)



                if email_lists:
                    #removing any empty
                    email_lists = filter(None, email_lists)
                    #removing duplicate
                    email_lists = list(set(email_lists))
                    message.add_bcc(email_lists)
            else:
                to_group = SentMessage.SEND_IND
                message.add_to(to_mail)
                email_lists = to_mail

            message.set_subject(subject_mail)
            message.set_html(content_mail)
            message.set_text(content_mail)

            #TODO logged in user here - once you implement the authentication, you can enable following like
            #from_email = request.user.email
            from_email = 'sashaseifollahi@gmail.com'
            message.set_from(from_email)

            if message.bcc or message.to:
                status, msg = sg.send(message)
                if to_group != SentMessage.SEND_IND:
                    email_lists = ','.join(map(str, email_lists))
                if status == 200:
                    save_email(request, to_group, email_lists, email_lists, email_lists, from_email, subject_mail, content_mail, content_mail, SentMessage.STATUS_SENT, msg)
                    messages.success(request, 'Your email was successfully sent.')
                else:
                    save_email(request, to_group, email_lists, email_lists, email_lists, from_email, subject_mail, content_mail, content_mail, SentMessage.STATUS_FAILED, msg)
                    messages.error(request, msg)
            else:
                messages.error(request, 'No emails are present')
    else:
        form = EMailForm(choices=get_send_choices(request))

    return render(request, 'messages/messages_page.html', {
        'form': form,
    })

def sent_mail(request):
    #getting sent mail for logged in user
    #Once authentication is implemented, you can use below instead getting all
    #sent_messages = SentMessage.objects.filter(sender=UserProfile.objects.get(user=request.user))
    sent_messages = SentMessage.objects.all().order_by('-created')

    paginator = Paginator(sent_messages, 10) # Show 10 contacts per page
    page = request.GET.get('page')

    try:
        sent_messages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sent_messages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        sent_messages = paginator.page(paginator.num_pages)

    return render(request, 'messages/sent_mail.html', {'sent_messages': sent_messages})
    