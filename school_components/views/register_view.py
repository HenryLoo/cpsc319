from school_components.models.courses_model import Course, Prerequisite, Department
from school_components.forms.courses_form import CourseForm, DepartmentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def course_register(request, page_no=None):
	if page_no is None or page_no == "1" :
		html = "registration/course_registration_parent.html"
	elif page_no == "2":
		html = "registration/course_registration_student.html"
	elif page_no == "3":
		html = "registration/course_registration_summary.html"
	elif page_no == "4":
		html = "registration/course_registration_payment.html"

	return render_to_response(html, {}, RequestContext(request))

def lkccourse_register(request, page_no=None):
	if page_no is None or page_no == "1" :
		html = "registration/lkc_course_registration_parent.html"
	elif page_no == "2":
		html = "registration/lkc_course_registration_student.html"
	elif page_no == "3":
		html = "registration/lkc_course_registration_summary.html"
	elif page_no == "4":
		html = "registration/lkc_course_registration_payment.html"

	return render_to_response(html, {}, RequestContext(request))