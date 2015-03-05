from django.views import generic
from school_components.models.parents_model import Parent
from school_components.models.students_model import Student
from school_components.forms.parents_form import ParentForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect


def parent_list(request):
	parent_list = Parent.objects.all()
	context_dictionary = {'parent_list': parent_list}

	return render_to_response("parents/base_parent.html",
		context_dictionary,
		RequestContext(request))

def parent_detail(request, parent_id):
	parent_list = Parent.objects.all()
	parent = Parent.objects.get(pk=parent_id)
	children = Student.objects.filter(parent=parent_id)

	context_dictionary = {'parent_list': parent_list, 
						'parent': parent,
						'children_list': children }
	return render_to_response('parents/parent_detail.html',
		context_dictionary,
		RequestContext(request))

def parent_create(request):
	p = ParentForm(request.POST)

	if p.is_valid():
		p.save()
		return HttpResponseRedirect('parent_list')
	else:
		parent_list = Parent.objects.all()
		context_dictionary = {'parent_list': parent_list,
							 'parent_form': ParentForm(),
							 'errors': p.errors }

		return render_to_response('parents/parent_form.html',
			context_dictionary,
			RequestContext(request))


def parent_form(request):
	parent_list = Parent.objects.all()
	context_dictionary = {'parent_list': parent_list,
						'parent_form': ParentForm() }

	return render_to_response('parents/parent_form.html',
		context_dictionary,
		RequestContext(request))
