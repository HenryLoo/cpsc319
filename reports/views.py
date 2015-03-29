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
from school_components.views.classes_view import find_overall_performance, find_class_performance
from school_components.forms.classes_form import *
from reports.forms import *
from accounts.utils import *

import datetime 
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required

# import weasyprint
# from weasyprint import HTML
# from django.template.loader import get_template

# try:
#     from StringIO import StringIO
# except ImportError:
#     from io import StringIO

# def pdf_view(request, class_id=None):

	#render_to_string(self.template_name, context, context_instance=RequestContext(self.request))

	# html = HTML(string="reports/mytemplate.html")
	# main_doc = html.render()
	# pdf = main_doc.write_pdf()
	# return HttpResponse(pdf, content_type='application/pdf')

    # class_list = Class.objects.filter(school = request.user_school, period = request.user_period).order_by('course')
    # context_dictionary = { 'class_list': class_list }

    # if class_id:
    #     c = Class.objects.get(pk=class_id)
    #     context_dictionary['class'] = c

    # render_to_string("reports/mytemplate.html", context, context_instance=RequestContext(self.request))

    # template = get_template("reports/mytemplate.html")
    # context = {"title": "A PDF"}
    # html = template.render(RequestContext(request, context))
    # response = HttpResponse(mimetype="application/pdf")
    # weasyprint.HTML(string=html).write_pdf(response)
    # return response

@login_required
def view_reports(request):
    return render(request, "reports/view_reports.html")

@login_required
def reportcard_teacher(request, class_id=None, student_id=None):
        request = process_user_info(request)
	class_list = Class.objects.filter(school = request.user_school, period = request.user_period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
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
		# context_dictionary['overall'] = average
		context_dictionary['overall'] = find_class_performance(student_id, class_id)

	return render_to_response('reports/reportcard_teacher.html', context_dictionary, RequestContext(request))

@login_required
def reportcard_adm(request, student_id=None):
        request = process_user_info(request)
	#add filter after
	perf_list = []
	over=0
	overall_value = 0
	student_list = Student.objects.filter(school = request.user_school).order_by('last_name')

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
			perf_list.append(find_class_performance(s.id, c.reg_class.id))
			# assignments_list = Grading.objects.filter(reg_class=c, student=s)
			# if len(assignments_list) != 0:
			# 	cont = 0
			# 	for a in assignments_list:
			# 		cont = cont + a.performance
			# 	p = cont/len(assignments_list)
			# 	over = over + p
			# 	perf_list.append(p)
		
		# if len(class_reg) != 0:
		# 	overall_value = over/len(class_reg)
			
		context_dictionary['class_list'] = class_reg
		context_dictionary['performance_list'] = perf_list
		context_dictionary['overall'] = find_overall_performance(s.id)

	return render_to_response('reports/reportcard_adm.html', context_dictionary, RequestContext(request))

@login_required
def studentphone(request, class_id=None):
        request = process_user_info(request)
	class_list = Class.objects.filter(school = request.user_school, period = request.user_period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c

	return render_to_response('reports/student_phone.html', context_dictionary, RequestContext(request))

@login_required
def attendancelist(request, class_id=None):
        request = process_user_info(request)
	class_list = Class.objects.filter(school = request.user_school, period = request.user_period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c

		date_form = AttendanceDateForm()
		context_dictionary['dateform'] = date_form

		if request.method == "POST":
				mon= -1
				tue= -1
				wed= -1
				thu= -1
				fri= -1
				sat= -1
				sun= -1

				schedule = ClassSchedule.objects.get(sch_class=c, sch_class__school = request.user_school, sch_class__period = request.user_period)
				
				if schedule.monday == True:
					mon = 0
				if schedule.tuesday == True:
					tue = 1
				if schedule.wednesday == True:
					wed = 2
				if schedule.thursday == True:
					thu = 3
				if schedule.friday == True:
					fri = 4
				if schedule.saturday == True:
					sat = 5
				if schedule.sunday == True:
					sun = 6

				date_form = AttendanceDateForm(request.POST)
				inter_start = date_form['start_date'].value()
				inter_end = date_form['end_date'].value()

				context_dictionary['start_date_value'] = inter_start
				context_dictionary['end_date_value'] = inter_end

				date_form = AttendanceDateForm(initial={'start_date': inter_start, 'end_date': inter_end})
				context_dictionary['dateform'] = date_form
				
				start_date = datetime.datetime.strptime(inter_start, "%m/%d/%Y").date()
				end_date = datetime.datetime.strptime(inter_end, "%m/%d/%Y").date()

				delta = end_date - start_date

				date_list = []
				week_list = []
				for i in range(delta.days + 1):
					day = start_date + timedelta(days=i)
					if (day.weekday() == mon) or (day.weekday() == tue) or (day.weekday() == wed) or (day.weekday() == thu) or (day.weekday() == fri) or (day.weekday() == sat) or (day.weekday() == sun):
   						print (day)
   						date_list.append(day)
   						week_list.append(day.weekday())

				days_list = zip(date_list, week_list)
				context_dictionary['dayslist'] = days_list

				return render_to_response('reports/attendance.html', context_dictionary, RequestContext(request))

		else:
				date_form = AttendanceDateForm()
				# inter = date_form['date'].value()
				# if inter and '/' in inter:
				# 	x,y,z = inter.split('/')
				# 	date_value = z + "-" + x + "-" + y
				# else:
				# 	date_value = inter	
				
				context_dictionary['dateform'] = date_form

	return render_to_response('reports/attendance.html', context_dictionary, RequestContext(request))

@login_required
def create_new_report_page(request):
    return render(request, "reports/create_new_report_page.html")

@login_required
def student_pdf(c):
    c.drawString(100, 100, "Hello World")
    c = canvas.Canvas("student.pdf")
    student_pdf(c)
    c.showPage()
    c.save()

@login_required
def export_data(request):
        request = process_user_info(request)
	dataset = request.GET.get('dataset', None)
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)

	school = request.user_school
	period = request.user_period

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
		

	
