from school_components.models.courses_model import Course, Prerequisite, Department
from school_components.forms.courses_form import CourseForm, DepartmentForm
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def course_list(request, course_id=None):
	course_list = Course.objects.all().order_by('name')
	context_dictionary = {'course_list': course_list}

	if course_id:
		c = Course.objects.get(pk=course_id)
		context_dictionary['course'] = c
		p = Prerequisite.objects.filter(course=course_id)
		if len(p) == 1:
			context_dictionary['prereq'] = p[0].prereq
	return render_to_response("courses/course_list.html",
		context_dictionary,
		RequestContext(request))

def course_create(request):
	context_dictionary = { 'course_form': CourseForm() }
	if request.method == 'POST':
		cf = CourseForm(request.POST)
		if cf.is_valid():
			new = cf.save()

			if cf['prerequisite'].value() != '':
				prq = Course.objects.get(pk=cf['prerequisite'].value())
				p = Prerequisite(course=new, prereq=prq)
				p.save()

			return HttpResponseRedirect(
				reverse('school:courselist', args=(new.id,)))
		else:
			context_dictionary['errors'] = cf.errors 

	return render_to_response('courses/course_form.html',
		context_dictionary,
		RequestContext(request))


def dept_create(request):
	context_dictionary = {'dept_form': DepartmentForm()}
	if request.method == 'POST':
		df = DepartmentForm(request.POST)
		if df.is_valid():
			new = df.save()
			return HttpResponseRedirect(reverse('school:courselist'))
		else:
			context_dictionary['errors'] = df.errors 

	return render_to_response('courses/dept_form.html',
		context_dictionary,
		RequestContext(request))

def course_assignment(request):
	return render(request, 'courses/course_assignment.html')
