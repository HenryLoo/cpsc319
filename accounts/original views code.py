from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from accounts.models import Teachers
from accounts.forms import TeachersForm

from django.db.models import Q


def teacherstable_page(request):
    return_dict = {}
        
    activeteachers = Teachers.objects.filter(status='active')
        
    return_dict['active_teachers'] = activeteachers
    return_dict['active_teachers_list'] = False
        
    if activeteachers.count() > 0:
        return_dict['active_teachers_list'] = True
        
    return render("accounts/teacherstable_page.html",return_dict)


def create_teacher_page(request):

    return_dict = {}

    if request.method == 'POST':
                            
        #teachers_page = Teachers()
        teachers_form = TeachersForm(request.POST)
                                
        if teachers_form.is_valid():
	    teachers_form.save()
            #teachers_page = teachers_form.save(commit=False)
                
            #teachers.email = teachers_page.email
            #teachers.name = teachers_page.name
            #teachers.phone = teachers_page.phone
            #teachers.skill_level = teachers_page.skill_level
            #teachers.description = teachers_page.description
            #teachers.status = 'active'
            
            #teachers.save()
                
            return HttpResponseRedirect(reverse('teacherstable_page'))
      
        else:
            teachers_form = TeachersForm()
                        
        return_dict['teachersform'] = teachers_form
                        
    return render_to_response("accounts/create_teacher_page.html",return_dict,RequestContext(request))
