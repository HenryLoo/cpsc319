from django.shortcuts import render
from accounts.models import *
from accounts.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def create_teacher_view(request):

    user_ret = None
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        availability_form = AvailabilityForm(request.POST)
        
        if user_form.is_valid() and teacher_form.is_valid() and availability_form.is_valid():
            
            user = user_form.save()
            role = Role(role='TEACHER')
            teacher = teacher_form.save(commit=False)
            availability = availability_form.save()
            teacher.teaching_availability = availability
            teacher.user_info = user
            role.user_info = user

            teacher.save()
            role.save()
    
            user_ret = user

        else:
            #if invalid data was submitted, load the same forms, which will show error messages
            return render(request, 'teachers/create_teacher.html', {
                'user_form': user_form,
                'teacher_form': teacher_form,
                'availability_form': availability_form,
            })      


    #if no data is submitted or teacher is created, load blank forms
    user_form = MyUserCreationForm()
    teacher_form = TeacherForm()
    availability_form = AvailabilityForm()

    return_dict = {
        'user_form': user_form,
        'teacher_form': teacher_form,
        'availability_form': availability_form,
        'user_ret' : user_ret
    }
    return render(request, 'teachers/create_teacher.html', return_dict)


def create_admin_view(request):
    
    user_ret = None
    admin_created = False
    
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        admin_form = AdminForm(request.POST)

        if user_form.is_valid() and admin_form.is_valid():

            user = user_form.save()
            role = Role(role=admin_form.cleaned_data['admin_type'])
            admin = admin_form.save(commit=False)
            role.user_info = user
            admin.user_info = user
            role.save()
            admin.save()
            
            admin_created = True

            user_ret = user

        else:

            return render(request, 'create_admin.html', {
                'user_form': user_form,
                'admin_form': admin_form,
                'admin_created': admin_created
            })

    user_form = MyUserCreationForm()
    admin_form = AdminForm()

    return render(request, 'admins/create_admin.html', {
        'user_form': user_form,
        'admin_form': admin_form,
        'admin_created': admin_created,
        'user_ret' : user_ret
    })


def view_teachers_view (request, teacher_id=None):
	teacher_list = TeacherInfo.objects.all()
	context_dictionary = {'teacher_list': teacher_list}

	if teacher_id:
		context_dictionary['teacher'] = TeacherInfo.objects.get(pk=teacher_id)

	return render(request, "teachers/teacher_list.html",
		context_dictionary)

def export_teachers_view (request):
    return render(request, "teachers/teacher_export.html")

def upload_teachers_view (request):
    return render(request, "teachers/teacher_upload.html")

def view_admins_view (request, admin_id=None):
	admin_list = AdminInfo.objects.all()
	context_dictionary = {'admin_list': admin_list}

	if admin_id:
		context_dictionary['admin'] = AdminInfo.objects.get(pk=admin_id)

	return render(request, "admins/admin_list.html",
		context_dictionary)
    
def login_view(request):
    
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid(): 
            user = authenticate(username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user) 
                    return HttpResponseRedirect('/')
                    
                else:
                    return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your account has been disabled.' })

            else:
                return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your username or password is invalid.' })

        else:
            return render(request, 'login/login.html', {'login_form' : login_form })

    else:
        login_form = LoginForm()
        return render(request, 'login/login.html', {'login_form' : login_form})

            
        
