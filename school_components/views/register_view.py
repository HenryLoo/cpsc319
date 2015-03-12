from school_components.models.courses_model import Course, Prerequisite, Department, CourseRegistration
from school_components.forms.courses_form import CourseForm, DepartmentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def course_register(request):
	return render_to_response("registration/course_registration.html",
		{}, RequestContext(request))

def lkccourse_register(request):
	return render_to_response("registration/lkc_course_registration.html",
		{}, RequestContext(request))