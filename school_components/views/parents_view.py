from django.views import generic
from school_components.models import Parent, Payment, Student, School, Period
from school_components.forms.parents_form import *
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# from urllib import urlencode
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import json
from django.contrib.auth.decorators import login_required
from accounts.utils import *

@login_required
def parent_list(request, parent_id=None):
	request = process_user_info(request)
	filters_form, parent_list = parent_list_helper(request) 
	context_dictionary = {
		'parent_list': parent_list,
		'parent_filter': filters_form
	}

	if parent_id:
		# hack for errors returned from payment create
		errors = request.GET.get('error', None)
		if errors:
			context_dictionary['payment_error'] = errors

		try:
			p = Parent.objects.get(pk=parent_id)
			if p.school != request.user_school:
					raise ObjectDoesNotExist
			
			context_dictionary['parent'] = p
			context_dictionary['payment_form'] = PaymentForm()

		except ObjectDoesNotExist:
				context_dictionary['error'] = 'There is no parent with that id in this school.'

				#post = request.POST
				#payment_id = request.POST['payment_id']
		try:
			post = request.POST
			payment_id = request.POST['payment_id']
			try:
				pay = Payment.objects.get(pk=payment_id)
				epf = PaymentForm(instance=pay)
				context_dictionary['edit_payment_form'] = epf
				context_dictionary['payment_id'] = payment_id
				
			except ObjectDoesNotExist:
					pass
				
		except Exception: #exception thrown if no payment id
			pass
		
	context_dictionary['view_form'] = ParentViewForm(
		{'view': 'all' if request.GET.get('view', None) == 'all' else 'period'})

	return render_to_response("parents/parent_list.html",
		context_dictionary,
		RequestContext(request))

# returns parent list according to filters/period or total view
# also returns the form with fields populated with last filter
def parent_list_helper(request):
	parent_list = None
	view = request.GET.get('view', None)

	if view is None or view == 'period':
		parent_list = Parent.objects.filter(
			school = request.user_school,
			student__enrolled_student__period = request.user_period
		).annotate().order_by('last_name')
	elif view == 'all':
		parent_list = Parent.objects.all().order_by('last_name')

	search_name = request.GET.get('name', None)
	search_receipt = request.GET.get('receipt_no', None)  
	form = ParentFilter({'name': search_name, 'receipt_no': search_receipt})   

	if search_name:
		parent_list = parent_list.filter(
			Q(first_name__icontains=search_name) | 
			Q(last_name__icontains=search_name))

	if search_receipt:
		parent_list = parent_list.filter(
		payment__receipt_no__icontains=search_receipt)

	return form, parent_list

@login_required
def payment_edit(request, parent_id, payment_id):
	request = process_user_info(request)
	if request.method == 'POST':
		pay = Payment.objects.get(pk=payment_id)
		pf = PaymentForm(request.POST, instance=pay)
		
		if pf.is_valid():
			pf.save()
			
			if request.is_ajax():
				return HttpResponse("Payment edited successfully.")
			else:
				return HttpResponseRedirect(
					reverse('school:parentlist', args=(parent_id,)))
		else:
			if request.is_ajax():
				return HttpResponse("An error occurred. Payment was not edited.")
			else:
				url = "%s?%s" % (reverse('school:parentlist', args=(parent_id,)), 
					urlencode({'error':1}))
				return redirect(url)

@login_required
def parent_edit(request, parent_id):

	request = process_user_info(request)

	form, parent_list = parent_list_helper(request)
	context_dictionary = {'parent_list': parent_list}

	try:
		p = Parent.objects.get(pk=parent_id)
		
		if p.school != request.user_school:

				raise ObjectDoesNotExist
				
		context_dictionary['parent_id'] = parent_id
		context_dictionary['payment_form'] = PaymentForm() #ig
		context_dictionary['parent_filter'] = form

		parent_form = ParentForm(instance=p)
		if request.method == 'POST':
			parent_form = ParentForm(request.POST, instance = p)
			if parent_form.is_valid():
					parent_form.save()
					context_dictionary['succ']=True
			
		context_dictionary['parent_form']=parent_form

	except ObjectDoesNotExist:
		context_dictionary['error'] = 'There is no parent with this id in this school.'

	context_dictionary['view_form'] = ParentViewForm(
		{'view': 'all' if request.GET.get('view', None) == 'all' else 'period'})
			
	return render_to_response("parents/parent_edit.html",
		context_dictionary,
		RequestContext(request))


@login_required
def parent_get(request):
	request = process_user_info(request)
	if request.method == 'GET':
		parent_id = request.GET['parent_id']
		parent = Parent.objects.get(pk=parent_id)
		parent_json = serializers.serialize("json", [parent])
		# extract the fields we want
		parent_json = json.dumps(json.loads(parent_json)[0]['fields'])
		return HttpResponse(parent_json, content_type="application/json")

@login_required
def parent_create(request):
	request = process_user_info(request)
	p = ParentForm(request.POST)
	context_dictionary = { 'parent_form': ParentForm() }
	if request.method == 'POST':

		if p.is_valid():
			new = p.save(commit=False)
			new.school = request.user_school
			new.period = request.user_period
			new.save()

			return HttpResponseRedirect(
				reverse('school:parentlist', args=(new.id,)))
		else:
			context_dictionary['errors'] = p.errors 

	return render_to_response('parents/parent_form.html',
		context_dictionary,
		RequestContext(request))

@login_required
def parent_form(request):
	parent_list = Parent.objects.all()
	context_dictionary = {'parent_list': parent_list,
						'parent_form': ParentForm() }

	return render_to_response('parents/parent_form.html',
		context_dictionary,
		RequestContext(request))

@login_required
def payment_create(request, parent_id):
	request = process_user_info(request)
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
	
			else: 
				url = "%s?%s" % (reverse('school:parentlist', args=(parent_id,)), 
					urlencode({'error':1}))
				return redirect(url)

