from django.views import generic
from school_components.models.students_model import Student
from school_components.models.parents_model import Parent
from school_components.forms.students_form import StudentForm, StudentCSVForm
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


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

def student_upload(request):
	context_dictionary = {'form': StudentCSVForm()}

	if request.method == 'POST':
		form = StudentCSVForm(request.POST, request.FILES)
		student_csv = parse_csv(request.FILES['file'])
		context_dictionary['message'] = student_csv

	return render_to_response('students/student_upload.html',
		context_dictionary, RequestContext(request))


def parse_csv(file):
	result = []
	for line in file:
		result.append(line)
	return result
