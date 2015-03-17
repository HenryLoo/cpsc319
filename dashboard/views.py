from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from dashboard.models import Attendance
from dashboard.models import Grade
from dashboard.models import Chart
from dashboard.models import NotificationType

from accounts.models import UserProfile

from school_components.models import Class
#from school_components.models import ClassSchedule
from school_components.models import ClassRegistration
from school_components.models import ClassTeacher
from school_components.models import Course
from school_components.models import Parent
from school_components.models import Payment
from school_components.models import Period
from school_components.models import School
from school_components.models import Student

from django.db.models import Q

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Sum

import datetime

def statistics_page(request):
    
    return_dict = {}

    students = Student.objects.count()
    admins = UserProfile.objects.exclude(role='TEACHER').count()
    teachers = UserProfile.objects.filter(role='TEACHER').count()
    classes = Class.objects.count()
    courses = Course.objects.count()
    periods = Period.objects.count()
    schools = School.objects.count()

    paid_students = Student.objects.select_related('parent__payment').values_list('id', flat=True).distinct()
    registered_students = ClassRegistration.objects.values_list('student_id', flat=True).distinct()
    unregistered_paid_students = paid_students.exclude(pk__in = registered_students).count()
    payment_total = Payment.objects.aggregate(Sum('amount')).get('amount__sum')
    if payment_total is None:
        payment_total = "0.00"
    receipts = Payment.objects.all().order_by('-date')
    charts = Chart.objects.all().order_by('title')

    return_dict['statistics'] = [[students, admins, teachers, classes, courses, periods, schools],[unregistered_paid_students, payment_total, receipts], charts]
        
    return render_to_response("dashboard/statistics_page.html",return_dict,RequestContext(request))

def demostatistics_page(request):
    
    context_dictionary = {}
        
    return render_to_response("dashboard/demostatistics_page.html",context_dictionary,RequestContext(request))

def notifications_page(request):
    
    context_dictionary = {}
        
    return render_to_response("dashboard/notifications_page.html",context_dictionary,RequestContext(request))

def notifications_settings_page(request):
    
    return_dict = {}
    
    if request.method == 'POST':
        attendanceCond = request.POST.get("attendanceCond")
        attendanceText = request.POST.get("attendanceText")
        performanceCond = request.POST.get("performanceCond")
        performanceText = request.POST.get("performanceText")
        assignmentCond = request.POST.get("assignmentCond")
        assignmentText = request.POST.get("assignmentText")

        attendance = NotificationType.objects.filter(notification_type='Attendance')
        if attendance.count() == 0:
            attendance = NotificationType(notification_type='Attendance', condition=attendanceCond, content=attendanceText)
            attendance.save()
        else:
            attendance.update(condition=attendanceCond)
            attendance.update(content=attendanceText)

        performance = NotificationType.objects.filter(notification_type='Performance')
        if performance.count() == 0:
            performance = NotificationType(notification_type='Performance', condition=performanceCond, content=performanceText)
            performance.save()
        else:
            performance.update(condition=performanceCond)
            performance.update(content=performanceText)
            

        assignment = NotificationType.objects.filter(notification_type='Assignment')
        if assignment.count() == 0:
            assignment = NotificationType(notification_type='Assignment', condition=assignmentCond, content=assignmentText)
            assignment.save()
        else:
            assignment.update(condition=assignmentCond)
            assignment.update(content=assignmentText)

        return_dict['applied'] = 1

    preAttendance = NotificationType.objects.filter(notification_type='Attendance').get()
    prePerformance = NotificationType.objects.filter(notification_type='Performance').get()
    preAssignment = NotificationType.objects.filter(notification_type='Assignment').get()

    return_dict['settings'] = [preAttendance, prePerformance, preAssignment]

    return render_to_response("dashboard/notifications_settings_page.html",return_dict,RequestContext(request))

def classes_schedule_page(request):
    
    return_dict = {}

    today = datetime.datetime.today().strftime('%a')
    #classSchedule = ClassSchedule.objects.filter(weekday=today).order_by('start_time')
    #students = Student.objects.select_related('classschedule').distinct().count()
    #teachers = ClassTeacher.objects.select_related('classschedule').distinct.count()
    #classes = classSchedule.count()

    #return_dict['schedule'] = [classSchedule, students, teachers, classes]

    return render_to_response("dashboard/classes_schedule_page.html",return_dict,RequestContext(request))

def view_reports(request):
    
    context_dictionary = {}
        
    return render_to_response("reports/view_reports.html",context_dictionary,RequestContext(request))

def assignment(request):
    
    context_dictionary = {}
        
    return render_to_response("school_components/assignment.html",context_dictionary,RequestContext(request))


#def statistics_page(request):
#    
#    return_dict = {}
#    
#    classes = Attendance.objects.values_list('classID', flat=True).distinct().order_by('classID')
#    
#    return_dict['statistics'] = classes
#    
#    return render_to_response("dashboard/statistics_page.html",return_dict,RequestContext(request))
#
#def notifications_page(request):
#    
#    context_dictionary = {}
#        
#    return render_to_response("dashboard/notifications_page.html",context_dictionary,RequestContext(request))
#
#def classes_schedule_page(request):
#    
#    context_dictionary = {}
#        
#    return render_to_response("dashboard/classes_schedule_page.html",context_dictionary,RequestContext(request))


def attendance_page(request):
    return_dict = {}

    viewFilter = request.GET.get("viewFilter")
    presentStudents = 0
    absentStudents = 0
    if viewFilter == "all":
      presentStudents = Attendance.objects.filter(status=1).count()
      absentStudents = Attendance.objects.filter(status=0).count()
    else:
      presentStudents = Attendance.objects.filter(classID=viewFilter).filter(status=1).count()
      absentStudents = Attendance.objects.filter(classID=viewFilter).filter(status=0).count()
        
    return_dict['attendance'] = [['Present', presentStudents], ['Absent', absentStudents]]
        
    return render_to_response("dashboard/attendance_page.html",return_dict,RequestContext(request))

def grades_page(request):
    return_dict = {}
        
    fStudents = Grade.objects.filter(grade__range=(0,49)).count()
    dStudents = Grade.objects.filter(grade__range=(50,54)).count()
    cStudents = Grade.objects.filter(grade__range=(55,67)).count()
    bStudents = Grade.objects.filter(grade__range=(68,79)).count()
    aStudents = Grade.objects.filter(grade__range=(80,100)).count()

    return_dict['grades'] = [['A', aStudents], ['B', bStudents], ['C', cStudents], ['D', dStudents], ['F', fStudents]]
        
    return render_to_response("dashboard/grades_page.html",return_dict,RequestContext(request))

def custom_statistic_page(request):
    return_dict = {}

    if request.method == 'POST':
        chartId = request.POST.get("customChart")

        chart = Chart.objects.filter(id=chartId)
        title = chart.values('title')
        chartType = chart.values('chart_type')
        xAxis = chart.values('x_axis')
        yAxis = chart.values('y_axis')

        xAxisValues = 0
        yAxisValues = 0
        if xAxis == "DATE":
        	xAxisValues = Period.objects.filter(id=1).values('start_date')
        elif xAxis == "CLASSES":
        	xAxisValues = Attendance.objects.filter(status=0).count()
        elif xAxis == "STUDENTS":
        	xAxisValues = Grade.objects.filter(grade__range=(0,100))

        if yAxis == "NSTUDENTS":
        	yAxisValues = Attendance.objects.filter(status=1).count()
        elif yAxis == "NCLASSES":
        	yAxisValues = Attendance.objects.filter(status=0).count()
        elif yAxis == "NTEACHERS":
            yAxisValues = Grade.objects.filter(grade__range=(0,100))
        elif yAxis == "ATTENDANCE":
            yAxisValues = Grade.objects.filter(grade__range=(0,100))
        elif yAxis == "PERFORMANCE":
            yAxisValues = Grade.objects.filter(grade__range=(0,100))
            
        return_dict['customStat'] = [[[xAxis, xAxisValues], [yAxis, yAxisValues]], title, chartType]
        
    return render_to_response("dashboard/custom_statistic_page.html",return_dict,RequestContext(request))

def custom_statistic_created_page(request):
    return_dict = {}

    if request.method == 'POST':
        title = request.POST.get("title")
        xAxis = request.POST.get("xAxis")
        yAxis = request.POST.get("yAxis")
        chartType = request.POST.get("chartType")
        visibility = request.POST.get("visibility")
        # Need to replace this with actual school and periods
        school = School.objects.filter(id=1).get()
        period = Period.objects.filter(id=1).get()
        chart = Chart(title=title, school=school, period=period, chart_type=chartType, x_axis=xAxis, y_axis=yAxis, visibility=visibility)
        chart.save()

    return render_to_response("dashboard/custom_statistic_created_page.html",return_dict,RequestContext(request))