from school_components.models.courses_model import Course, Prerequisite, Department
from school_components.forms.courses_form import CourseForm, DepartmentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.formtools.wizard.views import SessionWizardView
from school_components.forms.registration_form import *
from school_components.models import *
from django.core.exceptions import ObjectDoesNotExist


FORMS = [	
	('parent_form', ParentContactRegistrationForm),
	('student_form', StudentRegistrationForm)
]

TEMPLATES = {
	'parent_form': "registration/course_registration_parent.html",
	'student_form': "registration/course_registration_student.html",
	'summary_form': "registration/course_registration_summary.html",
	'payment_form': "registration/course_registration_payment.html",
}

TESTTEMPLATES = {
	'parent_form': "registration/temp.html",
	'student_form': "registration/temp.html",
	'summary_form': "registration/temp.html",
	'payment_form': "registration/temp.html",
}

class CourseRegisterWizard(SessionWizardView):

	# put current school/period in kwargs to render courses dropdown
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


	# based on parent first and last names
	def create_parent(self, form):
		school_id = self.request.session['school_id']
		period_id = self.request.session['period_id']

		school = School.objects.get(pk=school_id)
		period = Period.objects.get(pk=period_id)

		if form.is_valid():
			form_data = form.cleaned_data

			try:
				parent = Parent.objects.get(
					first_name=form_data['first_name'], 
					last_name=form_data['last_name'])

				parent.cell_phone=form_data['cell_phone']
				parent.email=form_data['email']
				parent.school=school
				parent.period=period 
				parent.comments=form_data['parent_comments']

			except ObjectDoesNotExist:
				parent = Parent(
					first_name=form_data['first_name'], 
					last_name=form_data['last_name'],
					cell_phone=form_data['cell_phone'],
					email=form_data['email'],
					school=school,
					period=period, 
					comments=form_data['parent_comments']
				)

			parent.save()
			return parent, "%s %s was saved successfully. " % (parent.first_name, parent.last_name)
		else:
			return None, "%s %s could not be updated. " % (parent.first_name, parent.last_name)

	def create_student(self, parent, form):
		school_id = self.request.session['school_id']
		period_id = self.request.session['period_id']

		school = School.objects.get(pk=school_id)
		period = Period.objects.get(pk=period_id)

		if form.is_valid():
			form_data = form.cleaned_data

			try:
				student = Student.objects.get(
					first_name=form_data['first_name'], 
					last_name=form_data['last_name'])

				student.home_phone=form_data['home_phone']
				address = "{0}, {1} {2}".format(
					form_data['street_address'], form_data['city'], form_data['postal_code'])
				student.address=address
				student.email=form_data['email']
				student.birthdate=form_data['birthdate']
				student.allergies=form_data['allergies']
				student.comments=form_data['comments']
				student.parent = parent
				student.school=school
				student.period=period 

			except ObjectDoesNotExist:
				addr = "{0}, {1} {2}".format(
						form_data['street_address'], form_data['city'], 
						form_data['postal_code'])
				student = Student(
					first_name=form_data['first_name'], 
					last_name=form_data['last_name'],
					home_phone=form_data['home_phone'],
					birthdate=form_data['birthdate'],
					address=addr,
					email=form_data['email'],
					allergies=form_data['allergies'],
					comments=form_data['comments'],
					parent = parent,
					school=school,
					period=period
				)

			student.save()
			return student, "%s %s was saved successfully." % (student.first_name, student.last_name)
		else:
			return None, "%s %s could not be updated." % (student.first_name, student.last_name)

	# THINK OF SOMETHING BETTER 
	def register_classes(self, student, form):
		course_status = {}

		form_data = form.cleaned_data
		for field, value in form_data.iteritems():
			if type(value) is str and "id_" in value:
				class_id = int(value.split('id_')[-1])
				classs = Class.objects.get(pk=class_id)

				current_size = ClassRegistration.objects.filter(reg_class=classs).count()
				registered = current_size + 1 <= classs.class_size

				course_status['%s %s' % (classs.course.name, classs.section)] = registered

				reg = ClassRegistration(reg_class=classs, student=student, 
					registration_status=registered)
				reg.save()


	# process the data from the parent and student forms
	def done(self, form_list, **kwargs):
		context_dictionary = {}

		parent, context_dictionary['parent_message'] = self.create_parent(form_list[0])
		student, context_dictionary['student_message'] = self.create_student(parent, form_list[1])
		context_dictionary['course_status'] = self.register_classes(student, form_list[1])

		return render_to_response(
			"registration/course_registration_summary.html", 
			context_dictionary)



def payment_create(request, parent_id):
	return render_to_response("registration/course_registration_payment.html", 
		{}, RequestContext(request))

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