from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reports.models import Reports
from school_components.models import *
from accounts.models import TeacherUser
from django.core.exceptions import ObjectDoesNotExist
import csv
from django.shortcuts import render
from django.template import RequestContext
from school_components.models.classes_model import *
from school_components.models.students_model import Student
from school_components.forms.classes_form import *

def view_reports(request):
    return render(request, "reports/view_reports.html")

def reportcard_teacher(request, class_id=None, student_id=None):
	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		print('class')
		context_dictionary['class'] = c

	if student_id:
		s = Student.objects.get(pk=student_id)
		context_dictionary['student'] = s

		grading_list = Grading.objects.filter(student=s, reg_class=c).order_by('-assignment__date').reverse()
		context_dictionary['gradinglist'] = grading_list

		cont=0
		for g in grading_list:
			cont = cont + g.performance
		total = len(grading_list)
		if total!= 0:
			average = cont/total
		else:
			average = 0
		context_dictionary['overall'] = average

	return render_to_response('reports/reportcard_teacher.html', context_dictionary, RequestContext(request))

def reportcard_adm(request, student_id=None):
	#add filter after
	perf_list = []
	over=0
	overall_value = 0
	student_list = Student.objects.filter(school = request.user.userprofile.school).order_by('last_name')

	context_dictionary = {
		'student_list': student_list,
	}

	if student_id:
		s = Student.objects.get(pk=student_id)
		context_dictionary['student'] = s

		#class registration - take all classes
		class_reg = ClassRegistration.objects.filter(student=s)
		

		#for each class, take all assignments
		for c in class_reg:
			assignments_list = Grading.objects.filter(reg_class=c, student=s)
			if len(assignments_list) != 0:
				cont = 0
				for a in assignments_list:
					cont = cont + a.performance
				p = cont/len(assignments_list)
				over = over + p
				perf_list.append(p)
		
		if len(class_reg) != 0:
			overall_value = over/len(class_reg)
			
		context_dictionary['class_list'] = class_reg
		context_dictionary['performance_list'] = perf_list
		context_dictionary['overall'] = overall_value

	return render_to_response('reports/reportcard_adm.html', context_dictionary, RequestContext(request))

def studentphone(request, class_id=None):
	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c


	return render_to_response('reports/student_phone.html', context_dictionary, RequestContext(request))


def create_new_report_page(request):
    return render(request, "reports/create_new_report_page.html")

def student_pdf(c):
    c.drawString(100, 100, "Hello World")
    c = canvas.Canvas("student.pdf")
    student_pdf(c)
    c.showPage()
    c.save()

def export_data(request):
	dataset = request.GET.get('dataset', None)
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)

	school = request.user.userprofile.school
	period = request.user.userprofile.period

	if dataset == 'student':
		students = Student.objects.all().filter(
			school=school, 
			enrolled_student__reg_class__period = period)
		writer.writerow(['First Name', 'Last Name', 'Gender', 'Birthdate', 'Home Phone', 'Parent',
			'Allergies', 'Comments'])
		for student in students:
			writer.writerow(
				[student.first_name, student.last_name, student.gender, student.birthdate, 
				student.home_phone, student.parent, student.allergies, student.comments])

	elif dataset == 'parent':
		parents = Parent.objects.all().filter(
			school=school,
			student__enrolled_student__period = period
			).annotate().order_by('last_name')
		writer.writerow(['First Name', 'Last Name', 'Cell Phone', 'Email', 'Comments'])
		for parent in parents:
			writer.writerow(
				[parent.first_name, parent.last_name, parent.cell_phone, parent.email, 
				parent.comments])

	elif dataset == 'teacher':
		teachers = TeacherUser.objects.all().filter(school=school, period=period)
		writer.writerow(['First Name', 'Last Name', 'Phone', 'Email', 'Comments'])
		for teacher in teachers:
			writer.writerow(
				[teacher.user.user.first_name, teacher.user.user.last_name, 
				teacher.user.phone, teacher.user, teacher.comments])

	elif dataset == 'class':
		classes = Class.objects.all().filter(school=school, period=period)
		writer.writerow(['Course', 'Section', 'Description', 'Class Size', 
			'Waiting List Size' ,'Room', 'Teacher', 'Schedule'])
		for classs in classes:
			writer.writerow(
				[classs.course, classs.section, classs.description, classs.class_size, 
				classs.waiting_list_size, classs.room, 
				'& '.join([str(t.teacher) for t in classs.taught_class.all()]),
				classs.schedule ])

	elif dataset == 'course':
		courses = Course.objects.all().filter(school=school, period=period)
		writer.writerow(['Course Name', 'Department', 'Prerequisite', 'Description'])
		for course in courses:
			try:
				prereq = str(course.prerequisite_set.get())
			except ObjectDoesNotExist:
				prereq = None

			writer.writerow(
				[course.name, course.department, prereq, course.description ])
			
	response['Content-Disposition'] = 'attachment; filename="' + dataset + '.csv"'
	return response
		

	
