from django.views import generic
from school_components.models import Student, Parent, School, Period
from school_components.models.courses_model import *
from school_components.forms.students_form import StudentForm, StudentCSVForm, StudentFormSet
from school_components.utils import SchoolUtils
from django.shortcuts import render_to_response, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.servers.basehttp import FileWrapper
from aplus.settings import SAMPLE_CSV_PATH
from django.core import serializers
import json
import csv


def student_list(request, student_id=None):
	student_list = Student.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('last_name')
	context_dictionary = {'student_list': student_list}

	if student_id:
		student = Student.objects.get(pk=student_id)
		context_dictionary['student'] = student
		
		class_list = [class_history_helper(class_reg) for class_reg in student.enrolled_student.all()]
		context_dictionary['class_history_list'] = class_list

	return render_to_response("students/student_list.html",
		context_dictionary,
		RequestContext(request))

# turn into a dict to help with sorting in UI
def class_history_helper(class_reg):
	m = model_to_dict(class_reg)
	m['period'] = class_reg.reg_class.period.description
	m['id'] = class_reg.reg_class.id
	m['class_name'] = class_reg.reg_class
	return m

# returns student info, used on the registration page
def student_get(request):
	if request.method == 'GET':
		student_id = request.GET['student_id']
		student = Student.objects.get(pk=student_id)
		student_json = serializers.serialize("json", [student])

		# get class history for student
		class_list = [class_reg.reg_class for class_reg in 
			student.enrolled_student.all().order_by('reg_class')]
		context_dictionary = {'class_list': class_list }

		render_string = render_to_string(
			'registration/course_registration_classhistory.html',
			context_dictionary)

		student_json = json.loads(student_json)[0]['fields']
		student_json['class_history_html'] = render_string
		student_json_str = json.dumps(student_json)

		return HttpResponse(student_json_str, content_type="application/json")


# create a new student with form data
def student_create(request):
	s = StudentForm(request.POST)
	context_dictionary = { 'student_form': StudentForm() }

	if request.method == 'POST':
		if s.is_valid():
			student = s.save(commit=False)
			student.school = request.user.userprofile.school
			student.period = request.user.userprofile.period
			student.save()
			return HttpResponseRedirect(
					reverse('school:studentlist', args=(student.id,)))
		else:
			context_dictionary['errors'] = s.errors 

	return render_to_response('students/student_form.html',
		context_dictionary,
		RequestContext(request))


def student_form(request):
	context_dictionary = {'student_form': StudentForm() }

	return render_to_response('students/student_form.html',
		context_dictionary,
		RequestContext(request))


# TODO: if file is too big, save to disk instead
# if time figure out a way to confirm
def student_upload(request):
	context_dictionary = {'form': StudentCSVForm()}
	form = StudentCSVForm(request.POST, request.FILES)
	
	if request.method == 'POST' and 'file' in request.FILES:
		#  check for errors
		errors = SchoolUtils.validate_csv(request.FILES['file'])

		if errors:
			context_dictionary['errors'] = errors
		else:
			# actually save
			s = request.user.userprofile.school
			per = request.user.userprofile.period
			student_list = SchoolUtils.parse_csv(request.FILES['file'], school=s, period=per)
			context_dictionary['student_list'] = student_list

	return render_to_response('students/student_upload.html',
		context_dictionary, RequestContext(request))

def student_export(request):
	context_dictionary = {}

	if request.method == 'POST':
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="students.csv"'

		students = Student.objects.all()
		writer = csv.writer(response)
		for student in students:
			writer.writerow(
				[student.first_name, student.last_name, student.gender, student.birthdate, 
				student.home_phone, student.parent, student.parent.cell_phone, student.parent.email, 
				student.allergies])

		return response
	else:
		return render_to_response('students/student_export.html',
			context_dictionary,
			RequestContext(request))

def student_sample_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="sample_students.csv"'
	
	f = open(SAMPLE_CSV_PATH)
	response.write(f.read())
	f.close()

	return response
