from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reports.models import Reports
from school_components.models import *
from accounts.models import TeacherUser
from django.core.exceptions import ObjectDoesNotExist
import csv


def view_reports(request):
    return render(request, "reports/view_reports.html")

def reportcard_teacher(request):
    return render(request, "reports/reportcard_teacher.html")

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
		students = Student.objects.all().filter(school=school)
		writer.writerow(['First Name', 'Last Name', 'Gender', 'Birthdate', 'Home Phone', 'Parent',
			'Allergies', 'Comments'])
		for student in students:
			writer.writerow(
				[student.first_name, student.last_name, student.gender, student.birthdate, 
				student.home_phone, student.parent, student.allergies, student.comments])

	elif dataset == 'parent':
		parents = Parent.objects.all().filter(school=school)
		writer.writerow(['First Name', 'Last Name', 'Cell Phone', 'Email', 'Comments'])
		for parent in parents:
			writer.writerow(
				[parent.first_name, parent.last_name, parent.cell_phone, parent.email, 
				parent.comments])

	elif dataset == 'teacher':
		teachers = TeacherUser.objects.all().filter(school=school)
		writer.writerow(['First Name', 'Last Name', 'Phone', 'Email', 'Comments'])
		for teacher in teachers:
			writer.writerow(
				[teacher.user.user.first_name, teacher.user.user.last_name, 
				teacher.user.phone, teacher.user, teacher.comments])

	elif dataset == 'class':
		classes = Class.objects.all().filter(school=school)
		writer.writerow(['Course', 'Section', 'Description', 'Class Size', 
			'Waiting List Size' ,'Room', 'Teacher', 'Schedule'])
		for classs in classes:
			writer.writerow(
				[classs.course, classs.section, classs.description, classs.class_size, 
				classs.waiting_list_size, classs.room, 
				'& '.join([str(t.teacher) for t in classs.taught_class.all()]),
				classs.schedule ])

	elif dataset == 'course':
		courses = Course.objects.all().filter(school=school)
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
		

	
