from school_components.models.period_model import Period
from school_components.forms.periods_form import PeriodForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def period_list(request, period_id=None):
	period_list = Period.objects.all().order_by('description')
	context_dictionary = {'period_list': period_list}

	if period_id:
		c = Period.objects.get(pk=period_id)
		context_dictionary['period'] = c
	return render_to_response("periods/period_list.html",
		context_dictionary,
		RequestContext(request))

def period_create(request):
	period_list = Period.objects.all()
	context_dictionary = {'period_list': period_list,
							 'period_form': PeriodForm()}
	if request.method == 'POST':
		cf = PeriodForm(request.POST)
		if cf.is_valid():
			new = cf.save()

			return HttpResponseRedirect(
				reverse('school:periodlist', args=(new.id,)))
		else:
			context_dictionary['errors'] = cf.errors 

	return render_to_response('periods/period_form.html',
		context_dictionary,
		RequestContext(request))



