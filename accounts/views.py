from django.shortcuts import render
from accounts.models import *
from accounts.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

def create_teacher_view(request):

    user_ret = None
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        teacher_phone = TeacherProfileForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        availability_form = AvailabilityForm(request.POST)
        
        if user_form.is_valid() and teacher_phone.is_valid() and teacher_form.is_valid() and availability_form.is_valid():

            try:
                try_user = User.objects.get(username=user_form.cleaned_data['email'])
                error = 'That email already belongs to another user.'
                return render(request, 'teachers/create_teacher.html', {
                    'error': error,
                    'user_form': user_form,
                    'teacher_phone': teacher_phone,
                    'teacher_form': teacher_form,
                    'availability_form': availability_form,
                })    
            except ObjectDoesNotExist:
                    
                user = User(username=user_form.cleaned_data['email'], email=user_form.cleaned_data['email'],
                            first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'])
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                #user = user_form.save(username=self.cleaned_data['email'],commit=False)
                availability = availability_form.save()
                teacher = teacher_form.save(commit=False)
                teacher.teaching_availability = availability

                profile = teacher_phone.save(commit=False)
                profile.role = 'TEACHER'
                profile.user = user
                
                profile.save()
                #profile.school = current school
                #profile.period = current period
                
                teacher.user = profile
                #teacher.save()
                teacher.save()
                
                user_ret = user

        else:
            #if invalid data was submitted, load the same forms, which will show error messages
            return render(request, 'teachers/create_teacher.html', {
                'user_form': user_form,
                'teacher_phone': teacher_phone,
                'teacher_form': teacher_form,
                'availability_form': availability_form,
            })      


    #if no data is submitted or teacher is created, load blank forms
    user_form = MyUserCreationForm()
    teacher_phone = TeacherProfileForm()
    teacher_form = TeacherForm()
    availability_form = AvailabilityForm()

    return_dict = {
        'user_form': user_form,
        'teacher_phone': teacher_phone,
        'teacher_form': teacher_form,
        'availability_form': availability_form,
        'user_ret' : user_ret
    }
    return render(request, 'teachers/create_teacher.html', return_dict)


def create_admin_view(request):
    
    user_ret = None
    
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        admin_form = AdminProfileForm(request.POST)

        if user_form.is_valid() and admin_form.is_valid():

            user = User(username=user_form.cleaned_data['email'], email=user_form.cleaned_data['email'],
                            first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'])
            user.set_password(user_form.cleaned_data['password'])
            user.save()
                
            profile = admin_form.save(commit=False)
            profile.user = user
            #profile.school = current school
            #profile.period = current period
            profile.save()
        
            user_ret = user

        else:

            return render(request, 'admins/create_admin.html', {
                'user_form': user_form,
                'admin_form': admin_form
            })

    user_form = MyUserCreationForm()
    admin_form = AdminProfileForm()

    return render(request, 'admins/create_admin.html', {
        'user_form': user_form,
        'admin_form': admin_form,
        'user_ret' : user_ret
    })


def view_teachers_view (request, teacher_id=None):
	teacher_list = TeacherUser.objects.all()
	context_dictionary = {'teacher_list': teacher_list}

	if teacher_id:
            try:
                teacher = TeacherUser.objects.get(pk=teacher_id)
		context_dictionary['teacher'] = teacher
	    except ObjectDoesNotExist:
                pass

	return render(request, "teachers/teacher_list.html",
		context_dictionary)

def export_teachers_view (request):
    return render(request, "teachers/teacher_export.html")

def upload_teachers_view (request):
    return render(request, "teachers/teacher_upload.html")

def view_admins_view (request, admin_id=None):
	system_admin_list = UserProfile.objects.filter(role="SYSTEM_ADMIN")
	school_admin_list = UserProfile.objects.filter(role="SCHOOL_ADMIN")
	context_dictionary = {'system_admin_list': system_admin_list,
                              'school_admin_list': school_admin_list}

	if admin_id:
            try:
                admin = UserProfile.objects.get(pk=admin_id)
		if admin.role == 'SCHOOL_ADMIN' or admin.role == 'SYSTEM_ADMIN':   
                    context_dictionary['admin'] = admin
	    except ObjectDoesNotExist:
                pass

	return render(request, "admins/admin_list.html",
		context_dictionary)
    
def login_view(request):
    
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid(): 
            user = authenticate(username=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user) 
                    return HttpResponseRedirect('/dashboard/statistics')
                    
                else:
                    return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your account has been disabled.' })

            else:
                return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your email or password is invalid.' })

        else:
            return render(request, 'login/login.html', {'login_form' : login_form })

    else:
        login_form = LoginForm()
        return render(request, 'login/login.html', {'login_form' : login_form})

        
        
