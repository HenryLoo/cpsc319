from school_components.models.school_model import School
from school_components.forms.schools_form import SchoolForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
@login_required
def school_list(request, school_id=None):
	school_list = School.objects.all().order_by('title')
	context_dictionary = {'school_list': school_list}

	if school_id:
		c = School.objects.get(pk=school_id)
		context_dictionary['school'] = c
	return render_to_response("schools/school_list.html",
		context_dictionary,
		RequestContext(request))

@login_required
def school_create(request):
	school_list = School.objects.all()
	context_dictionary = {'school_list': school_list,
							 'school_form': SchoolForm()}
	if request.method == 'POST':
		cf = SchoolForm(request.POST)
		if cf.is_valid():
			new = cf.save()

			return HttpResponseRedirect(
				reverse('school:schoollist', args=(new.id,)))
		else:
			context_dictionary['errors'] = cf.errors 

	return render_to_response('schools/school_form.html',
		context_dictionary,
		RequestContext(request))

@login_required
def school_change(request, school_id=None):
	if school_id:

		new_school = School.objects.get(pk = school_id)
		request.user.userprofile.school = new_school
		request.user.userprofile.period = None
		request.user.userprofile.save()

	return render_to_response('schools/school_list.html',
		RequestContext(request))

@login_required
def school_edit(request, school_id): #there should always be an school_id here
    #!!! probably block off this view entirely for anybody but system admin !!!
    
        school_list = School.objects.all().order_by('title')
        context_dictionary = {'school_list': school_list}
        
        try:
                c = School.objects.get(pk=school_id)
                context_dictionary['school_id']=school_id
                if request.method == 'POST':
                        school_form = SchoolForm(request.POST, instance = c)
                        if school_form.is_valid():
                                school_form.save()
                                context_dictionary['success']=True
                else:
                        school_form = SchoolForm(instance = c)
                        
                context_dictionary['school_form'] = school_form
                
        except ObjectDoesNotExist:
                context_dictionary['error'] = 'There is no school with that id.'

        return render_to_response("schools/school_edit.html",
                        context_dictionary,
                        RequestContext(request))

'''
Delete School
'''
@login_required
def school_delete(request, school_id):
    School.objects.get(pk=school_id).delete()
    messages.success(request, "School has been deleted!")
    return redirect('school:schoollist')
