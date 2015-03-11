from django.views import generic
from school_components.models.parents_model import Parent, Payment
from school_components.models.students_model import Student
from school_components.forms.parents_form import ParentForm, PaymentForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.core.urlresolvers import reverse


def parent_list(request, parent_id=None):
	parent_list = Parent.objects.all()
	context_dictionary = {'parent_list': parent_list}

	if parent_id:
		context_dictionary['parent'] = Parent.objects.get(pk=parent_id)
		context_dictionary['children_list'] = Student.objects.filter(parent=parent_id)
		context_dictionary['payment_form'] = PaymentForm()

	return render_to_response("parents/parent_list.html",
		context_dictionary,
		RequestContext(request))

def parent_create(request):
	parent_list = Parent.objects.all()
	p = ParentForm(request.POST)
	context_dictionary = {'parent_list': parent_list,
							 'parent_form': ParentForm()}
	if request.method == 'POST':
		if p.is_valid():
			new = p.save()
			return HttpResponseRedirect(
				reverse('school:parentlist', args=(new.id,)))
		else:
			context_dictionary['errors'] = p.errors 

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

def payment_create(request, parent_id):
	if request.method == 'POST':
		pay = Payment(parent=Parent.objects.get(pk=parent_id))
		pf = PaymentForm(request.POST, instance=pay)
		
		if pf.is_valid():
			pf.save()

			return HttpResponseRedirect(
				reverse('school:parentlist', args=(parent_id,)))
		else:
			return render_to_response('parents/parent_form.html',
				{'errors': pf.errors },
				RequestContext(request))
