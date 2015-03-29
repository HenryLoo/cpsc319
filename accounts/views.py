from django.shortcuts import render
from accounts.models import *
from accounts.forms import *
from accounts.utils import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.forms import ChoiceField

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

#===================                  ======================= TEACHER
@login_required
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
                #user.set_password(user_form.cleaned_data['password'])
                user.password = user_form.cleaned_data['password']
                user.save()
                #user = user_form.save(username=self.cleaned_data['email'].lower(),commit=False)
                availability = availability_form.save()
                teacher = teacher_form.save(commit=False)
                teacher.teaching_availability = availability

                profile = teacher_phone.save(commit=False)
                profile.role = 'TEACHER'
                profile.school = request.user.userprofile.school
                profile.period = request.user.userprofile.period
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
    password = User.objects.make_random_password()
    user_form = MyUserCreationForm(initial={'password': password})
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

@login_required
def view_teachers_view (request, teacher_id=None):
    teacher_list = TeacherUser.objects.filter(user__period=request.user.userprofile.period, user__school=request.user.userprofile.school)
    #teacher_list = TeacherUser.objects.all()
    
     # check if searching 
    search_name = request.GET.get('name', None)
    search_section = request.GET.get('class_section', None)
    search_course = request.GET.get('course', None)

    if search_name:
        teacher_list = teacher_list.filter(
            Q(user__user__first_name__icontains=search_name) |
            Q(user__user__last_name__icontains=search_name))
    if search_course:
        teacher_list = teacher_list.filter(
            teacher__taught_class__course__name__icontains=search_course
        )
    if search_section:
        teacher_list = teacher_list.filter(
            teacher__taught_class__section__icontains=search_section
        )

    context_dictionary = {'teacher_list': teacher_list,
                        'teacher_filter': TeacherFilterForm() }

    if teacher_id:
        try:
            teacher = TeacherUser.objects.get(pk=teacher_id)
            if not (request.user.userprofile.school == teacher.user.school and request.user.userprofile.period == teacher.user.period):
                raise ObjectDoesNotExist
            context_dictionary['teacher'] = teacher
        except ObjectDoesNotExist:
            context_dictionary['not_valid_teacher'] = True

    return render(request, "teachers/teacher_list.html",
        context_dictionary)

@login_required
def edit_teacher_view (request, teacher_id): #there should always be a teacher_id here
        teacher_list = TeacherUser.objects.filter(user__period=request.user.userprofile.period, user__school=request.user.userprofile.school)
        context_dictionary = {'teacher_list': teacher_list}

        try:
            teacher = TeacherUser.objects.get(pk=teacher_id)
            if not (request.user.userprofile.school == teacher.user.school and request.user.userprofile.period == teacher.user.period):
                raise ObjectDoesNotExist
            
            if request.method == 'POST': #assume if it was a post then the teacher exists, because otherwise a form wouldn't have appeared
                                        #!!!!! actually can't do that, imagine if teacher is deleted by another admin while on this page

                user_profile = teacher.user
                user = teacher.user.user
                availability = teacher.teaching_availability
                
                teacher_form = TeacherForm(request.POST, instance = teacher)
                teacher_phone = TeacherProfileForm(request.POST, instance = user_profile)
                user_form = MyUserCreationForm(request.POST, instance = user)
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
                context_dictionary['user_form'] = MyUserCreationForm(instance=teacher.user.user)
                context_dictionary['availability_form'] = AvailabilityForm(instance=teacher.teaching_availability)    
                
        except ObjectDoesNotExist:
             pass #template will display error message

        return render(request, "teachers/edit_teacher.html",
                   context_dictionary)


'''
Delete Teacher
'''
@login_required
def delete_teacher_view (request, teacher_id):
    teacher = TeacherUser.objects.get(pk=teacher_id)
    #deleting user profile
    profile = UserProfile.objects.get(id=teacher.user.id)
    profile.user.delete()
    profile.delete()
    teacher.delete()
    messages.success(request, "Teacher has been deleted!")
    return redirect('account:view_teachers')


@login_required
def upload_teachers_view(request):

    condict = {'upload_form' : TeacherCSVForm()}

    if request.method == 'POST':
        upload_form = TeacherCSVForm(request.POST, request.FILES)
        
        if not upload_form.is_valid():
            return render(request, "teachers/teacher_upload.html", {'upload_form' : upload_form })

        school = request.user.userprofile.school
        period = request.user.userprofile.period
        tlist, errors = validate_teachers_csv(request.FILES['file'], school, period)

        if errors:
            condict['errors'] = errors
        
        else:
            #save only if the csv had no errors
            teachers = []
            for t_tuple in tlist:
                user = t_tuple[0]
                profile = t_tuple[1]
                avail = t_tuple[2]
                teacher = t_tuple[3]

                user.save()
                profile.user = user
                profile.save()
                teacher.user = profile
                avail.save()
                teacher.teaching_availability = avail
                teacher.save()
                
                teachers.append(teacher)

            condict['teacher_list'] = teachers

        
    return render(request, "teachers/teacher_upload.html", condict)

@login_required
def export_teachers_view (request):
    return render(request, "teachers/teacher_export.html")

#==============================================================    ADMIN

@login_required
def create_admin_view(request):
    
    user_ret = None
    
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        admin_form = None
        if request.user.userprofile.role =='SCHOOL_ADMIN':
            admin_form = NoRoleAdminProfileForm(request.POST)
        elif request.user.userprofile.role =='SYSTEM_ADMIN':
            admin_form = AdminProfileForm(request.POST)

        if user_form.is_valid() and admin_form.is_valid():

            if not User.objects.filter(email=user_form.cleaned_data['email'].lower()).exists():
                
                user = User(username=user_form.cleaned_data['email'].lower(), email=user_form.cleaned_data['email'].lower(),
                                first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'])
                #user.set_password(user_form.cleaned_data['password'])
                user.password = user_form.cleaned_data['password']
                user.save()
                    
                profile = admin_form.save(commit=False)
                profile.user = user
                profile.school = request.user.userprofile.school
                profile.period = request.user.userprofile.period
                if request.user.userprofile.role == 'SCHOOL_ADMIN':
                    profile.role = 'SCHOOL_ADMIN'
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

    password = User.objects.make_random_password()
    user_form = MyUserCreationForm(initial={'password': password})
    admin_form = None
    if request.user.userprofile.role =='SCHOOL_ADMIN':
        admin_form = NoRoleAdminProfileForm()
    elif request.user.userprofile.role =='SYSTEM_ADMIN':
        admin_form = AdminProfileForm()
    
    
    
    return render(request, 'admins/create_admin.html', {
        'user_form': user_form,
        'admin_form': admin_form,
        'user_ret' : user_ret
    })

@login_required
def view_admins_view (request, admin_id=None):

    system_admin_list = UserProfile.objects.filter(role="SYSTEM_ADMIN")
    school_admin_list = UserProfile.objects.filter(role="SCHOOL_ADMIN", school=request.user.userprofile.school)
    context_dictionary = {'system_admin_list': system_admin_list,
                              'school_admin_list': school_admin_list}

    if admin_id:
        try:
            admin = UserProfile.objects.get(pk=admin_id)
            if admin.role == 'SCHOOL_ADMIN' or admin.role == 'SYSTEM_ADMIN':   #so as to not display teachers, if a teacher's userprofile id was entered in the url
                if admin.role == 'SCHOOL_ADMIN' and (not (request.user.userprofile.school == admin.school)):
                    raise ObjectDoesNotExist #school admin is from another school
                
                context_dictionary['admin'] = admin
            else:
                raise ObjectDoesNotExist #ie. admin is a teacher
        except ObjectDoesNotExist:
            context_dictionary['not_valid_id'] = True

    return render(request, "admins/admin_list.html",
        context_dictionary)

@login_required
def edit_admin_view (request, admin_id): #there should always be an admin_id here
    #!!! probably block off this view entirely for teachers !!!
    
        system_admin_list = UserProfile.objects.filter(role="SYSTEM_ADMIN")
        school_admin_list = UserProfile.objects.filter(role="SCHOOL_ADMIN", school=request.user.userprofile.school)
        context_dictionary = {'system_admin_list': system_admin_list,
                              'school_admin_list': school_admin_list}

        try:
            context_dictionary['error']='There is no admin with that id.'
            admin = UserProfile.objects.get(pk=admin_id)
            context_dictionary['error']=None
            
            #so as to not display teachers, if a teacher's userprofile id was entered in the url
            if not (admin.role == 'SCHOOL_ADMIN' or admin.role == 'SYSTEM_ADMIN'):
                context_dictionary['error']='There is no admin with that id.'
                raise ObjectDoesNotExist

            #to prevent editing school admins that aren't in the current school
            if admin.role == 'SCHOOL_ADMIN' and (not (request.user.userprofile.school == admin.user.userprofile.school)):
                context_dictionary['error']='You are not authorized to edit this admin.'
                raise ObjectDoesNotExist

            #to prevent school admins from editing system admins
            if admin.role == 'SYSTEM_ADMIN' and request.user.userprofile.role == 'SCHOOL_ADMIN':
                context_dictionary['error']='You are not authorized to edit this admin.'
                raise ObjectDoesNotExist

            
            if request.method == 'POST': #assume if it was a post then the admin exists, because otherwise a form wouldn't have appeared
                                        #!!!!! actually can't do that, imagine if this admin is deleted by another admin while on this page
                user = admin.user
                
                admin_form = NoRoleAdminProfileForm(request.POST, instance = admin)
                user_form = MyUserCreationForm(request.POST, instance = user)

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
                context_dictionary['admin_form'] = NoRoleAdminProfileForm(instance=admin) #hope these come with pre-filled fields
                context_dictionary['user_form'] = MyUserCreationForm(instance=admin.user)
                
        except ObjectDoesNotExist:
            
             pass #template will display error message because there's no admin

        return render(request, "admins/edit_admin.html",
                   context_dictionary)




'''
Delete Admin
'''
@login_required
def delete_admin_view (request, admin_id):
    admin = UserProfile.objects.get(pk=admin_id)
    admin.user.delete()
    admin.delete()
    messages.success(request, "Admin has been deleted!")
    return redirect('account:view_admins')

##============================================================  LOGIN
        
def login_view(request):
    
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['email'].lower(), password=login_form.cleaned_data['password'])
            #user = User.objects.all().filter(username=login_form.cleaned_data['email'].lower(), password=login_form.cleaned_data['password'])
            if user is not None:
            #if user.exists():
                #the_user = user[0]
                if user.is_active:
                    login(request, user) 
                    print (user.userprofile.school)
                    if user.userprofile.school != None:
                        if user.userprofile.role == 'TEACHER':
                            return HttpResponseRedirect('/dashboard/classes_schedule')
                        else:
                            return HttpResponseRedirect('/dashboard/statistics')
                    else:
                        return HttpResponseRedirect('/school/schools')
                    
                else:
                    return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your account has been disabled.' })

            else:
                return render(request, 'login/login.html', {'login_form' : login_form, 'error' : 'Your email or password is invalid.' })

        else:
            return render(request, 'login/login.html', {'login_form' : login_form })

    else:
        login_form = LoginForm()
        return render(request, 'login/login.html', {'login_form' : login_form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/account/login/')
        
        
