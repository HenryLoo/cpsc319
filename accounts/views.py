from django.shortcuts import render
from accounts.models import *
from accounts.forms import *
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def create_teacher_view(request):

    user_ret = None
    if request.method == 'POST':

        teacher_form = TeacherForm(request.POST)
        
        if teacher_form.is_valid():
            
            user = (teacher_form.save()).user_info
    
            user_ret = user

        else:
            #if invalid data was submitted, load the same forms, which will show error messages
            return render(request, 'teachers/create_teacher.html', {
                'teacher_form': teacher_form,
            })      


    #if no data is submitted or teacher is created, load blank forms
    teacher_form = TeacherForm()

    return_dict = {
        'teacher_form': teacher_form,
        'user_ret' : user_ret
    }
    return render(request, 'teachers/create_teacher.html', return_dict)


def create_admin_view(request):
    
    user_ret = None
    
    if request.method == 'POST':

        admin_form = AdminForm(request.POST)

        if admin_form.is_valid():

            user = admin_form.save()
            
            user_ret = user

        else:

            return render(request, 'admins/create_admin.html', {
                'admin_form': admin_form,
            })

    admin_form = AdminForm()

    return render(request, 'admins/create_admin.html', {
        'admin_form': admin_form,
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
	system_admin_list = User.objects.filter(role="SYS")
	school_admin_list = User.objects.filter(role="SCH")
	context_dictionary = {'system_admin_list': system_admin_list,
                              'school_admin_list': school_admin_list}
	if admin_id:
		context_dictionary['admin'] = User.objects.get(pk=admin_id)

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
                    return HttpResponseRedirect('/')
                    
                else:
                    return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your account has been disabled.' })

            else:
                return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your email does not belong to any account, or your password is incorrect.' })

        else:
            return render(request, 'login/login.html', {'login_form' : login_form })

    else:
        login_form = LoginForm()
        return render(request, 'login/login.html', {'login_form' : login_form})

            
        
