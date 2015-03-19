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

#===================                  ======================= TEACHER
def create_teacher_view(request):

    user_ret = None
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        teacher_phone = TeacherProfileForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        availability_form = AvailabilityForm(request.POST)
        
        if user_form.is_valid() and teacher_phone.is_valid() and teacher_form.is_valid() and availability_form.is_valid():

            try:
                try_user = User.objects.get(username=user_form.cleaned_data['email'].lower())
                error = 'That email already belongs to another user.'
                return render(request, 'teachers/create_teacher.html', {
                    'error': error,
                    'user_form': user_form,
                    'teacher_phone': teacher_phone,
                    'teacher_form': teacher_form,
                    'availability_form': availability_form,
                })    
            except ObjectDoesNotExist:
                    
                user = User(username=user_form.cleaned_data['email'].lower(), email=user_form.cleaned_data['email'].lower(),
                            first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'])
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                #user = user_form.save(username=self.cleaned_data['email'].lower(),commit=False)
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


def view_teachers_view (request, teacher_id=None):

	teacher_list = TeacherUser.objects.all()
	context_dictionary = {'teacher_list': teacher_list}

	if teacher_id:
            try:
                teacher = TeacherUser.objects.get(pk=teacher_id)
		context_dictionary['teacher'] = teacher
	    except ObjectDoesNotExist:
                context_dictionary['not_valid_teacher'] = True

	return render(request, "teachers/teacher_list.html",
		context_dictionary)

def edit_teacher_view (request, teacher_id): #there should always be a teacher_id here
    	teacher_list = TeacherUser.objects.all()
	context_dictionary = {'teacher_list': teacher_list}

        try:
            teacher = TeacherUser.objects.get(pk=teacher_id)
            
            if request.method == 'POST': #assume if it was a post then the teacher exists, because otherwise a form wouldn't have appeared
                                        #!!!!! actually can't do that, imagine if teacher is deleted by another admin while on this page

                user_profile = teacher.user
                user = teacher.user.user
                availability = teacher.teaching_availability
                
                teacher_form = TeacherForm(request.POST, instance = teacher)
                teacher_phone = TeacherProfileForm(request.POST, instance = user_profile)
                user_form = MyUserEditForm(request.POST, instance = user)
                availability_form = AvailabilityForm(request.POST, instance = availability)

                context_dictionary['teacher'] = teacher
                context_dictionary['teacher_form'] = teacher_form
                context_dictionary['teacher_phone'] = teacher_phone
                context_dictionary['user_form'] = user_form
                context_dictionary['availability_form'] = availability_form   

                if teacher_form.is_valid() and teacher_phone.is_valid() and user_form.is_valid() and availability_form.is_valid():
                    #check if a user other than yourself has this email
                    if not User.objects.exclude(pk=user.pk).filter(username=user_form.cleaned_data['email'].lower()).exists(): 
                
                        teacher_form.save()
                        teacher_phone.save()
                        user_form.save()
                        availability_form.save()
                        
                        user.username = user_form.cleaned_data['email'].lower()
                        user.save()
                        
                        context_dictionary['edit_success'] = True;

                    else:
                        error = 'That email already belongs to another user.'
                        context_dictionary['error'] = error;

                #user.set_password(user_form.cleaned_data['password'])
                #user.save()

                #data = user_form.cleaned_data
                #data['password'] = user.password #set it to the password hash
                #user_form = MyUserEditForm(data)
                #context_dictionary['user_form'] = user_form
                
            else:

                context_dictionary['teacher'] = teacher
                context_dictionary['teacher_form'] = TeacherForm(instance=teacher) #hope these come with pre-filled fields
                context_dictionary['teacher_phone'] = TeacherProfileForm(instance=teacher.user)
                context_dictionary['user_form'] = MyUserEditForm(instance=teacher.user.user)
                context_dictionary['availability_form'] = AvailabilityForm(instance=teacher.teaching_availability)    
                
        except ObjectDoesNotExist:
             pass #template will display error message

        return render(request, "teachers/edit_teacher.html",
                   context_dictionary)


def export_teachers_view (request):
    return render(request, "teachers/teacher_export.html")

def upload_teachers_view (request):
    return render(request, "teachers/teacher_upload.html")


#==============================================================    ADMIN

def create_admin_view(request):
    
    user_ret = None
    
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        admin_form = AdminProfileForm(request.POST)

        if user_form.is_valid() and admin_form.is_valid():

            if not User.objects.filter(email=user_form.cleaned_data['email'].lower()).exists():
                
                user = User(username=user_form.cleaned_data['email'].lower(), email=user_form.cleaned_data['email'].lower(),
                                first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'])
                user.set_password(user_form.cleaned_data['password'])
                user.save()
                    
                profile = admin_form.save(commit=False)
                profile.user = user
                #profile.school = current school
                #profile.period = current period
                profile.save()
            
                user_ret = user

                #if everything is good, return blank forms and the created user (below)

            else:
                #if email is taken, return filled forms with the error
                
                error = 'There is already a user with this email.'

                return render(request, 'admins/create_admin.html', {
                    'user_form': user_form,
                    'admin_form': admin_form,
                    'error': error
                })
                
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

def edit_admin_view (request, admin_id): #there should always be a teacher_id here
    	system_admin_list = UserProfile.objects.filter(role="SYSTEM_ADMIN")
	school_admin_list = UserProfile.objects.filter(role="SCHOOL_ADMIN")
	context_dictionary = {'system_admin_list': system_admin_list,
                              'school_admin_list': school_admin_list}

        try:
            admin = UserProfile.objects.get(pk=admin_id)
            
            if request.method == 'POST': #assume if it was a post then the teacher exists, because otherwise a form wouldn't have appeared
                                        #!!!!! actually can't do that, imagine if teacher is deleted by another admin while on this page
                user = admin.user
                
                admin_form = AdminProfileForm(request.POST, instance = admin)
                user_form = MyUserEditForm(request.POST, instance = user)

                context_dictionary['admin'] = admin
                context_dictionary['admin_form'] = admin_form
                context_dictionary['user_form'] = user_form

                if user_form.is_valid() and admin_form.is_valid():
                    #check if a user other than yourself has this email
                    if not User.objects.exclude(pk=user.pk).filter(username=user_form.cleaned_data['email'].lower()).exists(): 
                
                        user_form.save()
                        admin_form.save()
                        
                        user.username = user_form.cleaned_data['email'].lower()
                        user.save()
                        
                        context_dictionary['edit_success'] = True;

                    else:
                        error = 'That email already belongs to another user.'
                        context_dictionary['error'] = error;

                #user.set_password(user_form.cleaned_data['password'])
                #user.save()

                #data = user_form.cleaned_data
                #data['password'] = user.password #set it to the password hash
                #user_form = MyUserEditForm(data)
                #context_dictionary['user_form'] = user_form
                
            else:

                context_dictionary['admin'] = admin
                context_dictionary['admin_form'] = AdminProfileForm(instance=admin) #hope these come with pre-filled fields
                context_dictionary['user_form'] = MyUserEditForm(instance=admin.user)
                
        except ObjectDoesNotExist:
             pass #template will display error message because there's no admin

        return render(request, "admins/edit_admin.html",
                   context_dictionary)


##============================================================  LOGIN
    
def login_view(request):
    
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid(): 
            user = authenticate(username=login_form.cleaned_data['email'].lower(), password=login_form.cleaned_data['password'])
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

        
        
