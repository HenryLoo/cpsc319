from school_components.models.classes_model import Class, ClassRegistration
from school_components.forms.classes_form import ClassForm, ClassRegistrationForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# would like to render to class_reg.html and then load wih ajax
def class_list(request, class_id=None):
	class_list = Class.objects.all().order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c
		request.session['class'] = class_id
		context_dictionary['reg_list'] = ClassRegistration.objects.filter(reg_class=class_id)

	return render_to_response("classes/class_list.html",
		context_dictionary,
		RequestContext(request))

def class_create(request):
	context_dictionary = {'class_form': ClassForm()}
	if request.method == 'POST':
		cf = ClassForm(request.POST)
		if cf.is_valid():
			new = cf.save()

			return HttpResponseRedirect(
				reverse('school:classlist', args=(new.id,)))
		else:
			context_dictionary['errors'] = cf.errors 

	return render_to_response('classes/class_form.html',
		context_dictionary,
		RequestContext(request))

def class_registration(request):
	class_id = int(request.session['class'])
	context_dictionary = {
		'class': Class.objects.get(pk=class_id), 
		'reg_list': ClassRegistration.objects.filter(reg_class=class_id),
		'reg_form': ClassRegistrationForm() }

	return render_to_response("classes/class_registration.html",
		context_dictionary,
		RequestContext(request))
