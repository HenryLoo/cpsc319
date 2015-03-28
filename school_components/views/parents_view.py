from django.views import generic
from school_components.models import Parent, Payment, Student, School, Period
from school_components.forms.parents_form import ParentForm, PaymentForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json


def parent_list(request, parent_id=None):
	parent_list = Parent.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('last_name')
	context_dictionary = {'parent_list': parent_list}

	if parent_id:
		context_dictionary['parent'] = Parent.objects.get(pk=parent_id)
		context_dictionary['payment_form'] = PaymentForm()

	return render_to_response("parents/parent_list.html",
		context_dictionary,
		RequestContext(request))

def parent_edit(request, parent_id):
	parent_list = Parent.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('last_name')
	context_dictionary = {'parent_list': parent_list}

	try:
                p = Parent.objects.get(pk=parent_id)
                if p.school != request.user.userprofile.school or p.period != request.user.userprofile.period:
                        raise ObjectDoesNotExist
                
		context_dictionary['parent_id'] = parent_id
		context_dictionary['payment_form'] = PaymentForm() #ig
		parent_form = ParentForm(instance=p)
		if request.method == 'POST':
                        parent_form = ParentForm(request.POST, instance = p)
                        if parent_form.is_valid():
                                parent_form.save()
                                context_dictionary['succ']=True
                context_dictionary['parent_form']=parent_form

        except ObjectDoesNotExist:
                context_dictionary['error'] = 'There is no parent with this id in this school and period.'
                
	return render_to_response("parents/parent_edit.html",
		context_dictionary,
		RequestContext(request))


def parent_get(request):
	if request.method == 'GET':
		parent_id = request.GET['parent_id']
		parent = Parent.objects.get(pk=parent_id)
		parent_json = serializers.serialize("json", [parent])
		# extract the fields we want
		parent_json = json.dumps(json.loads(parent_json)[0]['fields'])
		return HttpResponse(parent_json, content_type="application/json")


def parent_create(request):
	p = ParentForm(request.POST)
	context_dictionary = { 'parent_form': ParentForm() }
	if request.method == 'POST':

		if p.is_valid():
			new = p.save(commit=False)
			new.school = request.user.userprofile.school
			new.period = request.user.userprofile.period
			new.save()

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
			
			if request.is_ajax():
				return HttpResponse("Payment added successfully.")
			else:
				return HttpResponseRedirect(
					reverse('school:parentlist', args=(parent_id,)))
		else:
			if request.is_ajax():
				return HttpResponse("An error occurred. Payment was not made.")
			return render_to_response('parents/parent_list.html',
				{'errors': pf.errors },
				RequestContext(request))

def payment_edit(request, parent_id, payment_id):
	if request.method == 'POST':
		pay = Payment.objects.get(pk=payment_id)
		pf = PaymentForm(request.POST, instance=pay)
		
		if pf.is_valid():
			pf.save()
			
			if request.is_ajax():
				return HttpResponse("Payment added successfully.")
			else:
				return HttpResponseRedirect(
					reverse('school:parentlist', args=(parent_id,)))
		else:
			if request.is_ajax():
				return HttpResponse("An error occurred. Payment was not made.")
			return render_to_response('parents/parent_list.html',
				{'errors': pf.errors },
				RequestContext(request))
