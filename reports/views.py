from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reports.models import Reports
from school_components.models import *
from django.db import connection


def view_reports(request):
    return render(request, "reports/view_reports.html")

# fn for generate the class list in the dropdown menu
def class_list(request, class_id=None):
	class_list = Class.objects.all().order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c
	print class_list
	return render_to_response('reports/view_reports.html',
			context_dictionary,
			RequestContext(request))

# fn for generate the section list according to the class above in the dropdown menu   
def find_section(request, class_id=None):
    search_text = request.POST['course_name']
    courses = Course.objects.filter(name = search_text)
    print courses
    c = Class.objects.filter(course = courses)[1]
    print c
    section_num = c.section.get()
    return render('reports/view_reports.html',
                   {'section_num': section_num})

# fn for searching the st_name and phone # according to the given class name + section #
def search_st(request):
    print "1"
    if request.method == 'POST':
        print "2"
        search_text = request.POST['course_name']
        search_num = request.POST['section']
    else:
        print "3"
        search_text = ''
    courses = Course.objects.filter(name = search_text)
    c = Class.objects.get(course = courses, section = search_num)
    context_dictionary = {"c":c}
    print search_text
    print courses
    print c
    print context_dictionary
    print [class_reg.student for class_reg in c.enrolled_class.all()]
    return render('reports/view_reports.html',
                  {'c': c})

# fn for searching students' names and each attendance
# according to the given class name,section # and range of dates
def search_attendance(request):
    if request.method == "POST":
        start_date = request.post['start_date']
        end_date = request.post['end_date']
        search_text = request.POST['course_name']
        search_num = request.POST['section']
        search_st = request.POST['st_name']
        
    courses = Course.objects.filter(name = search_text)
    c = Class.objects.get(course = courses, section = search_num)
    class_attendance = ClassAttendance.objects.get(Class_reg_class= c,
                                                   date__gte= start_date,
                                                   date__lte= end_date,
                                                   Student_name= search_st)
    print class_attendance
    return render_to_response('reports/view_reports.html',
			context_dictionary,
			RequestContext(request))
    
    
            
