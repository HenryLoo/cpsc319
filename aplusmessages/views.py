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
from django.contrib.auth.decorators import login_required
from accounts.utils import *

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
    request = process_user_info(request)
    user_choices = SentMessage.SEND_CHOICES

    '''
    adding departments
    '''
    for dep in Department.objects.filter(school = request.user_school).order_by('name'):
        dep = ("DEP#"+str(dep.id), dep.name, )
        user_choices = user_choices + (dep,)

    '''
    adding courses
    '''

    for course in Course.objects.filter(school = request.user_school, period = request.user_period).order_by('name'):
        course = ("COURSE#"+str(course.id), course.name, )
        user_choices = user_choices + (course,)

    '''
    adding classes
    '''

    for sc_class in Class.objects.filter(school = request.user_school,  period = request.user_period).order_by('course'):
        sc_class = ("CLASS#"+str(sc_class.id), sc_class.section, )
        user_choices = user_choices + (sc_class,)

    return user_choices



'''
sends email to selected group of people or to individual
'''
@login_required
def send_email(request):
    request = process_user_info(request)
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
                    email_lists = Student.objects.filter(school = request.user_school, period = request.user_period).order_by('last_name').values_list('email', flat=True)
                elif to_group == SentMessage.SEND_TEACHERS:
                    '''
                    teachers are selected
                    '''
                    email_lists = TeacherUser.objects.filter(user__period=request.user_period, user__school=request.user_school).values_list('user__user__email', flat=True)
                elif to_group == SentMessage.SEND_ADMINS:
                    '''
                    admins are selected
                    '''
                    system_admin_list = UserProfile.objects.filter(role="SYSTEM_ADMIN").values_list('user__email', flat=True)
                    school_admin_list = UserProfile.objects.filter(role="SCHOOL_ADMIN", school=request.user_school).values_list('user__email', flat=True)

                    for sysemail in system_admin_list:
                        email_lists.append(sysemail)

                    for scemail in school_admin_list:
                        email_lists.append(scemail)

                elif to_group == SentMessage.SEND_EVERYONE:
                    #TODO Add additional filters here if required
                    email_lists = []

                    for semail in Student.objects.filter(school = request.user_school, period = request.user_period).order_by('last_name').values_list('email', flat=True):
                        email_lists.append(semail)

                    for temail in TeacherUser.objects.filter(user__period=request.user_period, user__school=request.user_school).values_list('user__user__email', flat=True):
                        email_lists.append(temail)

                    system_admin_list = UserProfile.objects.filter(role="SYSTEM_ADMIN").values_list('user__email', flat=True)
                    school_admin_list = UserProfile.objects.filter(role="SCHOOL_ADMIN", school=request.user_school).values_list('user__email', flat=True)

                    for sysemail in system_admin_list:
                        email_lists.append(sysemail)

                    for scemail in school_admin_list:
                        email_lists.append(scemail)

                #if departement
                elif to_group.startswith('DEP'):
                   #getting department id
                    dep_id = to_group.split("#")
                    dep_id = dep_id[1]

                    #getting all students from departments
                    dep = Department.objects.get(pk=dep_id)
                    # getting eveything individually in order to avoid join, which in turn improve performance
                    courses = Course.objects.filter(department=dep).values_list('id', flat=True)
                    classes = Class.objects.filter(course__in=courses).values_list('id', flat=True)
                    registrations = ClassRegistration.objects.filter(reg_class__in=classes).values_list('student__id', flat=True)
                    email_lists = Student.objects.filter(id__in=registrations).values_list('email', flat=True)

                #if course
                elif to_group.startswith('COURSE'):
                   #getting course id
                    course_id = to_group.split("#")
                    course_id = course_id[1]

                    #getting all students for course
                    courses = Course.objects.get(id=course_id)
                    #getting eveything individually in order to avoid join, which in turn improve performance
                    classes = Class.objects.filter(course=courses).values_list('id', flat=True)
                    registrations = ClassRegistration.objects.filter(reg_class__in=classes).values_list('student__id', flat=True)
                    email_lists = Student.objects.filter(id__in=registrations).values_list('email', flat=True)

                #if class
                elif to_group.startswith('CLASS'):
                   #getting course id
                    class_id = to_group.split("#")
                    class_id = class_id[1]

                    #getting all students for class
                    classes = Class.objects.get(pk=class_id)
                    #getting eveything individually in order to avoid join, which in turn improve performance
                    registrations = ClassRegistration.objects.filter(reg_class=classes).values_list('student__id', flat=True)
                    email_lists = Student.objects.filter(id__in=registrations).values_list('email', flat=True)


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

            from_email = request.user.email
            #from_email = 'sashaseifollahi@gmail.com'
            message.set_from(from_email)

            if message.bcc or message.to:
                status, msg = sg.send(message)

                if to_group != SentMessage.SEND_IND:
                    email_lists = ','.join(map(str, email_lists))

                to_st = dict(get_send_choices(request)).get(to_group, to_group)
                if status == 200:
                    save_email(request, to_st, email_lists, email_lists, email_lists, from_email, subject_mail, content_mail, content_mail, SentMessage.STATUS_SENT, msg)
                    messages.success(request, 'Your email was successfully sent.')
                else:
                    save_email(request, to_st, email_lists, email_lists, email_lists, from_email, subject_mail, content_mail, content_mail, SentMessage.STATUS_FAILED, msg)
                    messages.error(request, msg)
            else:
                messages.error(request, 'No emails are present')
    else:
        form = EMailForm(choices=get_send_choices(request))

    return render(request, 'messages/messages_page.html', {
        'form': form,
    })

@login_required
def sent_mail(request):
    request = process_user_info(request)
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
    
