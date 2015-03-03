from django.views import generic
from school_components.models.students_model import Student, StudentCSVWriter
from school_components.models.parents_model import Parent
from school_components.forms.students_form import StudentForm, StudentCSVForm, StudentFormSet
from school_components.utils import SchoolUtils
from django.shortcuts import render_to_response, redirect
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import csv


def student_list(request):
	student_list = Student.objects.all()
	context_dictionary = {'student_list': student_list}

	return render_to_response("students/base_student.html",
		context_dictionary,
		RequestContext(request))

# should probably replace with ajax
def student_detail(request, student_id):
	student_list = Student.objects.all()
	student = Student.objects.get(pk=student_id)

	context_dictionary = {'student_list': student_list, 
						'student': student }
	return render_to_response('students/student_detail.html',
		context_dictionary,
		RequestContext(request))


# create a new student with form data
def student_create(request):
	s = StudentForm(request.POST)

	if s.is_valid():
		new = s.save()
		return HttpResponseRedirect(
			reverse('school:studentdetail', args=(new.id,)))
	else:
		student_list = Student.objects.all()
		context_dictionary = {'student_list': student_list,
							 'student_form': StudentForm(),
							 'errors': s.errors }

		return render_to_response('students/student_form.html',
		context_dictionary,
		RequestContext(request))


def student_form(request):
	student_list = Student.objects.all()

	context_dictionary = {'student_list': student_list,
							'student_form': StudentForm() }

	return render_to_response('students/student_form.html',
		context_dictionary,
		RequestContext(request))

#  would be nice if to ask for confirmation first...
def student_upload(request):
	context_dictionary = {'form': StudentCSVForm()}

	if request.method == 'POST':
		form = StudentCSVForm(request.POST, request.FILES)
		student_list = SchoolUtils.parse_csv(request.FILES['file'])
		context_dictionary['message'] = 'These students were created.'
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
			writer.writerow([student.first_name, student.last_name, 
				student.gender, student.birthdate, student.home_phone])

		return response
	else:
		return render_to_response('students/student_export.html',
			context_dictionary,
			RequestContext(request))




