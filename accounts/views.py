from django.shortcuts import render
from accounts.models import *
from accounts.forms import *
from django.contrib.auth.forms import UserCreationForm

def create_teacher(request):

    teacher_created = False
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        availability_form = AvailabilityForm(request.POST)
        
        if user_form.is_valid() and teacher_form.is_valid() and availability_form.is_valid():
            
            user = user_form.save()
            role = User(role='TEACHER')
            teacher = teacher_form.save(commit=False)
            availability = availability_form.save()
            teacher.teaching_availability = availability
            teacher.user_info = user
            role.user_info = user

            teacher.save()
            role.save()

            teacher_created = True

        else:
            #if invalid data was submitted, load the same forms, which hopefully will show error messages
            return render(request, 'accounts/create_teacher.html', {
                'user_form': user_form,
                'teacher_form': teacher_form,
                'availability_form': availability_form,
                'teacher_created': teacher_created
            })      


    #if no data is submitted, or teacher is created successfully, load blank forms
    user_form = MyUserCreationForm()
    teacher_form = TeacherForm()
    availability_form = AvailabilityForm()

    return render(request, 'accounts/create_teacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form,
        'availability_form': availability_form,
        'teacher_created': teacher_created
    })

def create_admin(request):

    admin_created = False
    
    if request.method == 'POST':

        user_form = MyUserCreationForm(request.POST)
        admin_form = AdminForm(request.POST)

        if user_form.is_valid() and admin_form.is_valid():

            user = user_form.save()
            role = User(role=admin_form.cleaned_data['admin_type'])
            admin = admin_form.save(commit=False)
            role.user_info = user
            admin.user_info = user
            role.save()
            admin.save()
            
            admin_created = True

        else:

            return render(request, 'create_admin.html', {
                'user_form': user_form,
                'admin_form': admin_form,
                'admin_created': admin_created
            })

    user_form = MyUserCreationForm()
    admin_form = AdminForm()

    return render(request, 'create_admin.html', {
        'user_form': user_form,
        'admin_form': admin_form,
        'admin_created': admin_created
    })
        
#old views
def teacherstable_page(request):
    return_dict = {}
        
    activeteachers = Teachers.objects.filter(status='active')
        
    return_dict['active_teachers'] = activeteachers
    return_dict['active_teachers_list'] = False
        
    if activeteachers.count() > 0:
        return_dict['active_teachers_list'] = True
        
    return render("accounts/teacherstable_page.html",return_dict)  
        
