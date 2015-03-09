from school_components.models.school_model import School
from school_components.forms.schools_form import SchoolForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def school_list(request, school_id=None):
	school_list = School.objects.all().order_by('title')
	context_dictionary = {'school_list': school_list}

	if school_id:
		c = School.objects.get(pk=school_id)
		context_dictionary['school'] = c
	return render_to_response("schools/school_list.html",
		context_dictionary,
		RequestContext(request))

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



