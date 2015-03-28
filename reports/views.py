from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reports.models import Reports
from django.shortcuts import render
from django.template import RequestContext

from school_components.models.classes_model import *
from school_components.models.students_model import Student
from school_components.forms.classes_form import *
from reports.forms import *

import datetime 
from datetime import date, timedelta

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

    # class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
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


def view_reports(request):
    return render(request, "reports/view_reports.html")

def reportcard_teacher(request, class_id=None, student_id=None):
	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
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


def attendancelist(request, class_id=None):
	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
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

				schedule = ClassSchedule.objects.get(sch_class=c, sch_class__school = request.user.userprofile.school, sch_class__period = request.user.userprofile.period)
				
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

def create_new_report_page(request):
    return render(request, "reports/create_new_report_page.html")

def student_pdf(c):
    c.drawString(100, 100, "Hello World")
    c = canvas.Canvas("student.pdf")
    student_pdf(c)
    c.showPage()
    c.save()
