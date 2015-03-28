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
