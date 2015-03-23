from school_components.models.classes_model import Class, ClassRegistration
from school_components.models.students_model import Student
from school_components.forms.classes_form import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse

def class_list(request, class_id=None):
	class_list = Class.objects.filter(
		school = request.user.userprofile.school, 
		period = request.user.userprofile.period).order_by('course')
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

		if cf.is_valid() and sf.is_valid():
			# save class
			new = cf.save(commit=False)
			new.school = request.user.userprofile.school
			new.period = request.user.userprofile.period
			new.save()

			# save class schedule
			schedule = sf.save(commit=False)
			schedule.sch_class = new
			schedule.save()

			# save class teacher
			try:
				te = ClassTeacherForm(request.POST, prefix='te')
				if te.is_valid():
					teacher = te.save(commit=False)
					teacher.taught_class = new
					teacher.save()
			except Exception as e:
				# no teacher in request, don't create ClassTeacher object
				pass

			return HttpResponseRedirect(
				reverse('school:classlist', args=(new.id,)))
		else:
			context_dictionary['class_errors'] = cf.errors
			context_dictionary['schedule_errors'] = sf.errors
			context_dictionary['teacher_errors'] = te.errors

	return render_to_response('classes/class_form.html',
		context_dictionary,
		RequestContext(request))

def class_registration(request, class_id=None):
	if request.POST:
		# register student in class
		student_id = request.GET['student_id']
		student = Student.objects.get(pk=student_id)
		classs = Class.objects.get(pk=class_id) 
		school = request.user.userprofile.school
		period = request.user.userprofile.period

		try:
			cr = ClassRegistration(
				reg_class=classs, student=student, registration_status=True,
				school=school, period=period)
			cr.save()
			return HttpResponse("Successfully registered.")

		except IntegrityError:
			return HttpResponse("That student is already registered.")

		except Exception as e:
			return HttpResponseBadRequest(e)

	else:
		class_list = Class.objects.filter(
			school = request.user.userprofile.school, 
			period = request.user.userprofile.period).order_by('course')
		context_dictionary = {'class_list': class_list }

		if class_id:
			cl = Class.objects.get(pk=class_id)
			context_dictionary['class'] = cl
			context_dictionary['student_list'] = Student.objects.all()
		
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
