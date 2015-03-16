from school_components.models.courses_model import Course, Prerequisite, Department
from school_components.forms.courses_form import CourseForm, DepartmentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from school_components.forms.registration_form import *

FORMS = [	
	('parent_form', ParentContactRegistrationForm),
	('student_form', StudentRegistrationForm),
	('summary_form', SummaryRegistrationForm),
	('payment_form', PaymentRegistrationForm)
]

TEMPLATES = {
	'parent_form': "registration/temp.html",
	'student_form': "registration/course_registration_student.html",
	'summary_form': "registration/course_registration_summary.html",
	'payment_form': "registration/course_registration_payment.html",
}

class CourseRegisterWizard(SessionWizardView):

	# get current school/period to render form
	def get_form_kwargs(self, step=None):
		kwargs = {}
		if step == 'student_form':
			kwargs = {
				'school_id': self.request.session['school_id'],
				'period_id': self.request.session['period_id'],
			}
		return kwargs

	def get_template_names(self):
			return [TEMPLATES[self.steps.current]]

	def done(self, form_list, **kwargs):
		return render_to_response("registration/temp.html",
			{'message': [form.data for form in form_list]}, 
			RequestContext(request))


def course_register(request, page_no=None):
	if page_no is None or page_no == "1" :
		html = "registration/course_registration_parent.html"
	elif page_no == "2":
		html = "registration/course_registration_student.html"
	elif page_no == "3":
		html = "registration/course_registration_summary.html"
	elif page_no == "4":
		html = "registration/course_registration_student.html"

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