from school_components.models.classes_model import Class, ClassRegistration
from school_components.forms.classes_form import *
from django.shortcuts import render_to_response
from django.shortcuts import render
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
	
	return render_to_response("classes/class_list.html",
		context_dictionary,
		RequestContext(request))

def class_create(request):
	context_dictionary = {
		'class_form': ClassForm(prefix='info'), 
		'classday_form': ClassScheduleForm(prefix='sch'),
		'classteacher_form': ClassTeacherForm(prefix='te')
	}
	if request.method == 'POST':
		cf = ClassForm(request.POST, prefix='info')
		sf = ClassScheduleForm(request.POST, prefix='sch')
		te = ClassTeacherForm(request.POST, prefix='te')

		if cf.is_valid() and sf.is_valid() and te.is_valid():
			# save class
			new = cf.save()

			# save class schedule
			schedule = sf.save(commit=False)
			schedule.sch_class = new
			schedule.save()

			# save class teacher
			teacher = te.save(commit=False)
			teacher.taught_class = new
			teacher.save()

			return HttpResponseRedirect(
				reverse('school:classlist', args=(new.id,)))
		else:
			context_dictionary['errors'] = cf.errors 

	return render_to_response('classes/class_form.html',
		context_dictionary,
		RequestContext(request))

def class_registration(request):
	#class_id = int(request.session['class'])
	# context_dictionary = {
	# 	'class': Class.objects.get(pk=class_id), 
	# 	'reg_list': ClassRegistration.objects.filter(reg_class=class_id),
	# 	'reg_form': ClassRegistrationForm() }
	context_dictionary ={}
	
	return render_to_response("classes/class_registration.html",
		context_dictionary,
		RequestContext(request))

def class_attendance(request):
	return render(request, 'classes/class_attendance.html')

def class_performance(request):
	return render(request, 'classes/class_grading.html')

def class_assignment(request):
	return render(request, 'classes/class_assignment.html')

def class_reportcard(request):
    return render(request, 'classes/class_reportcard.html')
