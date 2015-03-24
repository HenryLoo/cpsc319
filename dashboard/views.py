from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext

from dashboard.models import Chart, Notification, NotificationType

from accounts.models import UserProfile

from school_components.models import Class, ClassSchedule, ClassRegistration, ClassTeacher, Course, Grading, Parent, Payment, Period, School, Student

from django.db.models import Q

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Sum, Count

import datetime

from operator import attrgetter
from itertools import chain

from django.contrib.auth import authenticate, login

def statistics_page(request):
    
    return_dict = {}

    currentSchool = request.user.userprofile.school
    currentPeriod = request.user.userprofile.period

    if request.method == 'POST':
        title = request.POST.get("title")
        xAxis = request.POST.get("xAxis")
        yAxis = request.POST.get("yAxis")
        chartType = request.POST.get("chartType")
        visibility = request.POST.get("visibility")
        # Replaced by current
        school = currentSchool
        period = cuurentPeriod
        chart = Chart(title=title, school=school, period=period, chart_type=chartType, x_axis=xAxis, y_axis=yAxis, visibility=visibility)
        chart.save()
        return_dict['createdCustom'] = 1

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

    return_dict['usage'] = [students, admins, teachers, classes, courses, periods, schools]
    return_dict['payments'] = [unregistered_paid_students, payment_total, receipts]

    regXAxis = Period.objects.filter(school_id=currentSchool).all().order_by('start_date').values_list('description', flat=True)
    regYAxis = ClassRegistration.objects.filter(school_id=currentSchool).values_list('student_id', 'period_id').distinct().values('period_id').annotate(num_students=Count('period')).values_list('num_students', flat=True)
    return_dict['registrationChart'] = []
    for x in zip(regXAxis, regYAxis):
        return_dict['registrationChart'].append([x[0], x[1]])

    
    performance = Grading.objects.filter(reg_class__school=currentSchool, reg_class__period=currentPeriod).values('grade').order_by('grade').annotate(num_students=Count('grade'))   
    performXAxis = performance.values_list('grade', flat=True)
    performYAxis = performance.values_list('num_students', flat=True)
    return_dict['performanceChart'] = []
    for x in zip(performXAxis, performYAxis):
        return_dict['performanceChart'].append([x[0], x[1]])

    numPass = sum(performance.exclude(grade__range=[5, 10]).values_list('num_students', flat=True))
    try:
        numFail = performance.filter(grade__range=[0, 5]).values_list('num_students', flat=True).get()
    except:
        numFail = ''
    return_dict['passFailChart'] = [['Pass', numPass], ['Fail', numFail]]


    return_dict['chartTypeOptions'] = Chart._meta.get_field('chart_type').choices
    return_dict['xAxisOptions'] = Chart._meta.get_field('x_axis').choices
    return_dict['yAxisOptions'] = Chart._meta.get_field('y_axis').choices
    return_dict['visibilityOptions'] = Chart._meta.get_field('visibility').choices

    charts = Chart.objects.filter(school_id=currentSchool, period_id=currentPeriod)
    if request.user.userprofile == 'TEACHER':
        charts = charts.filter(visibility='ALL')
    charts = charts.all()

    # return_dict['customCharts'] = Student.objects.filter()
    return_dict['customChartsTriplets'] = []
    for i in range(0, len(charts), 3):
        return_dict['customChartsTriplets'].append(charts[i:i+3])

    # for chart in charts:
    #     xVar = ''
    #     if chart.x_axis == 'SCHOOL':
    #         xVar = 'school'
    #     elif chart.x_axis == 'PERIOD':
    #         xVar = 'period'
    #     elif chart.x_axis == 'CLASS':
    #         xVar = 'class'

    #     chartData = ''
    #     if chart.y_axis == 'NSTUDENTS':
    #         chartData = Student.objects.select_related(xVar)
    #     elif chart.y_axis == 'NCLASSES':
    #         #
    #     elif chart.y_axis == 'NTEACHERS':
    #         #
    #     elif chart.y_axis == 'ATTENDANCE':
    #         #
    #     elif chart.y_axis == 'PERFORMANCE':
    #         #

    #     return_dict['customCharts'].append([])

    return render_to_response("dashboard/statistics_page.html",return_dict,RequestContext(request))

# def demostatistics_page(request):
    
#     context_dictionary = {}
        
#     return render_to_response("dashboard/demostatistics_page.html",context_dictionary,RequestContext(request))

def notifications_page(request):
    
    return_dict = {}

    currentSchool = request.user.userprofile.school
    currentPeriod = request.user.userprofile.period

    if request.method == 'POST':
        for key in request.POST:
            if key != 'csrfmiddlewaretoken':
                notif = Notification.objects.filter(id=int(key))
                if request.POST.get(key) == 'Not Called':
                    notif.update(status=False)
                elif request.POST.get(key) == 'Called':
                    notif.update(status=True)

    allNotifications = Notification.objects.filter(school_id=currentSchool, period_id=currentPeriod).all().order_by('-date')
    notifications = allNotifications
    return_dict['filter'] = request.GET.get("filter")
    if return_dict['filter'] == '1':
        notifications = allNotifications.filter(status=False)
    elif return_dict['filter'] == '2':
        notifications = allNotifications.filter(status=True)
    else:
        notifications = allNotifications
    notificationTypes = []
    studentNames = []
    for notification in notifications:
        notificationTypes.append(NotificationType.objects.get(id=notification.notification_type_id))
        studentNames.append(Student.objects.get(id=notification.student_id))
    return_dict['numNew'] = allNotifications.filter(status=False).count()
    return_dict['numOld'] = allNotifications.filter(status=True).count()
    return_dict['numAll'] = return_dict['numNew'] + return_dict['numOld']

    return_dict['notifications'] = []
    for x in zip(notifications, notificationTypes, studentNames):
        return_dict['notifications'].append([x[0], x[1], x[2]])

    # pages = len(return_dict['notifications'])
    # currentPage = 1
    # pageRange = [currentPage, currentPage + 7]
    # 
    # currentPage = int(request.GET.get("currentPage"))
    # if currentPage + 7 > pages:
    #   pageRange = [pages - 7, pages]

    # return_dict['pages'] = [i for i in range(pageRange[0], pageRange[1])]
        
    return render_to_response("dashboard/notifications_page.html",return_dict,RequestContext(request))

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

    currentSchool = request.user.userprofile.school
    currentPeriod = request.user.userprofile.period

    return_dict['weekday'] = request.GET.get("weekday")
    if return_dict['weekday'] not in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        return_dict['weekday'] = datetime.datetime.today().strftime('%a')

    classSchedule = ClassSchedule.objects
    if return_dict['weekday'] == 'Mon':
        classSchedule = classSchedule.filter(monday=True)
    elif return_dict['weekday'] == 'Tue':
        classSchedule = classSchedule.filter(tuesday=True)
    elif return_dict['weekday'] == 'Wed':
        classSchedule = classSchedule.filter(wednesday=True)
    elif return_dict['weekday'] == 'Thu':
        classSchedule = classSchedule.filter(thursday=True)
    elif return_dict['weekday'] == 'Fri':
        classSchedule = classSchedule.filter(friday=True)
    elif return_dict['weekday'] == 'Sat':
        classSchedule = classSchedule.filter(saturday=True)
    elif return_dict['weekday'] == 'Sun':
        classSchedule = classSchedule.filter(sunday=True)
    classSchedule = classSchedule.order_by('start_time')

    if request.user.userprofile == 'TEACHER':
        teacherID = TeacherUser.filter(user_id=request.user.userprofile.user_id).get().teacher_id
        taughtClasses = ClassTeacher.filter(teacher_id=teacherID).values_list('taught_class_id', flat=True)
        classSchedule = classSchedule.filter(sch_class_id__in=taughtClasses)
    
    classTimes = classSchedule.values_list('start_time', 'end_time')
    courseIDs = []
    numStudents = []
    numTeachers = []
    classIDs = classSchedule.values_list('sch_class_id', flat=True)
    for x in classIDs:
        courseIDs.append(Class.objects.get(pk=x).course_id)
        numStudents.append(ClassRegistration.objects.filter(reg_class_id=x).count())
        numTeachers.append(ClassTeacher.objects.filter(taught_class_id=x).count())

    courseNames = []
    for x in courseIDs:
        courseNames.append(Course.objects.get(pk=x).name)

    return_dict['schedule'] = []
    for i in range(0, len(classTimes)):
        return_dict['schedule'].append([classTimes[i][0].strftime('%H:%M'), classTimes[i][1].strftime('%H:%M'), courseNames[i], numStudents[i], numTeachers[i], classIDs[i]])

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


# def attendance_page(request):
#     return_dict = {}

#     viewFilter = request.GET.get("viewFilter")
#     presentStudents = 0
#     absentStudents = 0
#     if viewFilter == "all":
#       presentStudents = Attendance.objects.filter(status=1).count()
#       absentStudents = Attendance.objects.filter(status=0).count()
#     else:
#       presentStudents = Attendance.objects.filter(classID=viewFilter).filter(status=1).count()
#       absentStudents = Attendance.objects.filter(classID=viewFilter).filter(status=0).count()
        
#     return_dict['attendance'] = [['Present', presentStudents], ['Absent', absentStudents]]
        
#     return render_to_response("dashboard/attendance_page.html",return_dict,RequestContext(request))

# def grades_page(request):
#     return_dict = {}
        
#     fStudents = Grade.objects.filter(grade__range=(0,49)).count()
#     dStudents = Grade.objects.filter(grade__range=(50,54)).count()
#     cStudents = Grade.objects.filter(grade__range=(55,67)).count()
#     bStudents = Grade.objects.filter(grade__range=(68,79)).count()
#     aStudents = Grade.objects.filter(grade__range=(80,100)).count()

#     return_dict['grades'] = [['A', aStudents], ['B', bStudents], ['C', cStudents], ['D', dStudents], ['F', fStudents]]
        
#     return render_to_response("dashboard/grades_page.html",return_dict,RequestContext(request))

# def custom_statistic_page(request):
#     return_dict = {}

#     if request.method == 'POST':
#         chartId = request.POST.get("customChart")

#         chart = Chart.objects.filter(id=chartId)
#         title = chart.values('title')
#         chartType = chart.values('chart_type')
#         xAxis = chart.values('x_axis')
#         yAxis = chart.values('y_axis')

#         xAxisValues = 0
#         yAxisValues = 0
#         if xAxis == "DATE":
#         	xAxisValues = Period.objects.filter(id=1).values('start_date')
#         elif xAxis == "CLASSES":
#         	xAxisValues = Attendance.objects.filter(status=0).count()
#         elif xAxis == "STUDENTS":
#         	xAxisValues = Grade.objects.filter(grade__range=(0,100))

#         if yAxis == "NSTUDENTS":
#         	yAxisValues = Attendance.objects.filter(status=1).count()
#         elif yAxis == "NCLASSES":
#         	yAxisValues = Attendance.objects.filter(status=0).count()
#         elif yAxis == "NTEACHERS":
#             yAxisValues = Grade.objects.filter(grade__range=(0,100))
#         elif yAxis == "ATTENDANCE":
#             yAxisValues = Grade.objects.filter(grade__range=(0,100))
#         elif yAxis == "PERFORMANCE":
#             yAxisValues = Grade.objects.filter(grade__range=(0,100))
            
#         return_dict['customStat'] = [[[xAxis, xAxisValues], [yAxis, yAxisValues]], title, chartType]
        
#     return render_to_response("dashboard/custom_statistic_page.html",return_dict,RequestContext(request))

# def custom_statistic_created_page(request):
#     return_dict = {}

#     if request.method == 'POST':
#         title = request.POST.get("title")
#         xAxis = request.POST.get("xAxis")
#         yAxis = request.POST.get("yAxis")
#         chartType = request.POST.get("chartType")
#         visibility = request.POST.get("visibility")
#         # Need to replace this with actual school and periods
#         school = School.objects.filter(id=1).get()
#         period = Period.objects.filter(id=1).get()
#         chart = Chart(title=title, school=school, period=period, chart_type=chartType, x_axis=xAxis, y_axis=yAxis, visibility=visibility)
#         chart.save()

#     return render_to_response("dashboard/custom_statistic_created_page.html",return_dict,RequestContext(request))
