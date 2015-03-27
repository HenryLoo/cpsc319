from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext

from dashboard.models import Chart, Notification, NotificationType

from accounts.models import UserProfile

from school_components.models import Class, ClassAttendance, ClassSchedule, ClassRegistration, ClassTeacher, Course, Grading, Parent, Payment, Period, School, Student

from django.db.models import Q

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Avg, Sum, Count

import datetime

from operator import attrgetter
from itertools import groupby

from django.contrib.auth import authenticate, login

def statistics_page(request):
    
    context_dictionary = {}

    currentSchool = request.user.userprofile.school
    currentPeriod = request.user.userprofile.period

    if request.method == 'POST':
        title = request.POST.get("title")
        xAxis = request.POST.get("xAxis")
        yAxis = request.POST.get("yAxis")
        chartType = request.POST.get("chartType")
        visibility = request.POST.get("visibility")
        school = currentSchool
        period = currentPeriod
        chart = Chart(title=title, school=school, period=period, chart_type=chartType, x_axis=xAxis, y_axis=yAxis, visibility=visibility)
        chart.save()
        context_dictionary['createdCustom'] = 1

    students = Student.objects.count()
    admins = UserProfile.objects.exclude(role='TEACHER').count()
    teachers = UserProfile.objects.filter(role='TEACHER').count()
    classes = Class.objects.count()
    courses = Course.objects.count()
    periods = Period.objects.count()
    schools = School.objects.count()

    paidParentIDs = Payment.objects.values_list('parent_id', flat=True)
    parentIDs = Parent.objects.filter(id__in=paidParentIDs, school_id=currentSchool, period_id=currentPeriod).values_list('id', flat=True)
    paidStudents = Student.objects.filter(parent_id__in=parentIDs).values_list('id', flat=True)
    registeredStudents = ClassRegistration.objects.values_list('student_id', flat=True).distinct()
    unregisteredPaidStudents = paidStudents.exclude(pk__in = registeredStudents).count()

    paymentTotal = Payment.objects.aggregate(Sum('amount')).get('amount__sum')
    if paymentTotal is None:
        paymentTotal = "0.00"
    receipts = Payment.objects.all().order_by('-date')

    context_dictionary['usage'] = [students, admins, teachers, classes, courses, periods, schools]
    context_dictionary['payments'] = [unregisteredPaidStudents, paymentTotal, receipts]

    regXAxis = Period.objects.filter(school_id=currentSchool).all().order_by('start_date').values_list('description', flat=True)
    regYAxis = ClassRegistration.objects.filter(school_id=currentSchool).values_list('student_id', 'period_id').distinct().values('period_id').annotate(num_students=Count('period')).values_list('num_students', flat=True)
    context_dictionary['registrationChart'] = []
    for x in zip(regXAxis, regYAxis):
        context_dictionary['registrationChart'].append([x[0], x[1]])

    
    performance = Grading.objects.filter(reg_class__school=currentSchool, reg_class__period=currentPeriod).values('student_id').annotate(avg_grades=Avg('performance'))
    gradeList = [round(grade) for grade in performance.order_by('avg_grades').values_list('avg_grades', flat=True)]
    performXAxis = list(set(gradeList))
    performYAxis = [len(list(group)) for key, group in groupby(gradeList)]
    context_dictionary['performXAxis'] = performXAxis
    context_dictionary['performYAxis'] = performYAxis
    context_dictionary['performanceChart'] = []
    for x in zip(performXAxis, performYAxis):
        context_dictionary['performanceChart'].append([x[0], x[1]])

    numPass = sum(grade >= 50 for grade in gradeList)
    numFail = sum(grade < 50 for grade in gradeList)
    context_dictionary['passFailChart'] = [['Pass', numPass], ['Fail', numFail]]

    context_dictionary['chartTypeOptions'] = Chart._meta.get_field('chart_type').choices
    context_dictionary['xAxisOptions'] = Chart._meta.get_field('x_axis').choices
    context_dictionary['yAxisOptions'] = Chart._meta.get_field('y_axis').choices
    context_dictionary['visibilityOptions'] = Chart._meta.get_field('visibility').choices

    charts = Chart.objects.filter(school_id=currentSchool, period_id=currentPeriod)
    if request.user.userprofile == 'TEACHER':
        charts = charts.filter(visibility='ALL')
    charts = charts.all().order_by('id')

    allChartData = []
    for chart in charts:
        xAxis = ''
        xIDs = ''
        xFilter = ''
        if chart.x_axis == 'SCHOOL':
            schools = School.objects.all()
            xAxis = schools.values_list('title', flat=True)
            xIDs = schools.values_list('id', flat=True)
            xFilter = 'school_id'
        elif chart.x_axis == 'PERIOD':
            periods = Period.objects.filter(school=currentSchool).all()
            xAxis = periods.values_list('description', flat=True)
            xIDs = periods.values_list('id', flat=True)
            xFilter = 'period_id'
        elif chart.x_axis == 'COURSE':
            courses = Course.objects.filter(school=currentSchool, period=currentPeriod)
            xAxis = courses.values_list('name', flat=True)
            xIDs = courses.values_list('id', flat=True)
            xFilter = 'course_id'

        yAxis = []
        classes = Class.objects
        for x in xIDs:
            filteredClassIDs = classes.filter(**{xFilter: x}).values_list('id', flat=True)
            if chart.y_axis == 'NSTUDENTS':
                yAxis.append(ClassRegistration.objects.filter(reg_class_id__in=filteredClassIDs).all().values('student_id').distinct().count())
            elif chart.y_axis == 'NCLASSES':
                yAxis.append(len(filteredClassIDs))
            elif chart.y_axis == 'NTEACHERS':
                yAxis.append(ClassTeacher.objects.filter(taught_class_id__in=filteredClassIDs).all().values('teacher_id').distinct().count())
            elif chart.y_axis == 'ATTENDANCE':
                allAttendance = ClassAttendance.objects.filter(reg_class_id__in=filteredClassIDs)
                numAttended = allAttendance.exclude(attendance='A').all().count()
                numTotal = allAttendance.all().count()
                if numTotal == 0:
                    numTotal = 1
                yAxis.append(round(sumAttended/numTotal))
            elif chart.y_axis == 'PERFORMANCE':
                averages = Grading.objects.filter(reg_class_id__in=filteredClassIDs).annotate(avg_grades=Avg('performance')).values_list('avg_grades', flat=True)
                yAxis.append(round(sum(averages)/len(averages)))

        chartData = []
        for x in zip(xAxis, yAxis):
            chartData.append([x[0], x[1]])
        allChartData.append(chartData)

    chartsWithData = []
    for x in zip(charts, allChartData):
        chartTypeField = x[0].chart_type
        chartTypeValue = ''
        if chartTypeField == 'BAR':
            chartTypeValue = 'BarChart'
        elif chartTypeField == 'PIE':
            chartTypeValue = 'PieChart'
        elif chartTypeField == 'LINE':
            chartTypeValue = 'LineChart'
        chartsWithData.append([x[0], x[1], chartTypeValue])

    context_dictionary['customChartsTriplets'] = []
    for i in range(0, len(chartsWithData), 3):
        context_dictionary['customChartsTriplets'].append(chartsWithData[i:i+3])

    return render_to_response("dashboard/statistics_page.html",context_dictionary,RequestContext(request))

# def demostatistics_page(request):
    
#     context_dictionary = {}
        
#     return render_to_response("dashboard/demostatistics_page.html",context_dictionary,RequestContext(request))

def notifications_page(request):
    
    context_dictionary = {}

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
    context_dictionary['filter'] = request.GET.get("filter")
    if context_dictionary['filter'] == '1':
        notifications = allNotifications.filter(status=False)
    elif context_dictionary['filter'] == '2':
        notifications = allNotifications.filter(status=True)
    else:
        notifications = allNotifications
    notificationTypes = []
    studentNames = []
    for notification in notifications:
        notificationTypes.append(NotificationType.objects.get(id=notification.notification_type_id))
        studentNames.append(Student.objects.get(id=notification.student_id))
    context_dictionary['numNew'] = allNotifications.filter(status=False).count()
    context_dictionary['numOld'] = allNotifications.filter(status=True).count()
    context_dictionary['numAll'] = context_dictionary['numNew'] + context_dictionary['numOld']

    context_dictionary['notifications'] = []
    for x in zip(notifications, notificationTypes, studentNames):
        context_dictionary['notifications'].append([x[0], x[1], x[2]])

    # pages = len(context_dictionary['notifications'])
    # currentPage = 1
    # pageRange = [currentPage, currentPage + 7]
    # 
    # currentPage = int(request.GET.get("currentPage"))
    # if currentPage + 7 > pages:
    #   pageRange = [pages - 7, pages]

    # context_dictionary['pages'] = [i for i in range(pageRange[0], pageRange[1])]
        
    return render_to_response("dashboard/notifications_page.html",context_dictionary,RequestContext(request))

def notifications_settings_page(request):
    
    context_dictionary = {}
    
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

        context_dictionary['applied'] = 1

    preAttendance = NotificationType.objects.filter(notification_type='Attendance').get()
    prePerformance = NotificationType.objects.filter(notification_type='Performance').get()
    preAssignment = NotificationType.objects.filter(notification_type='Assignment').get()

    context_dictionary['settings'] = [preAttendance, prePerformance, preAssignment]

    return render_to_response("dashboard/notifications_settings_page.html",context_dictionary,RequestContext(request))

def classes_schedule_page(request):
    
    context_dictionary = {}

    currentSchool = request.user.userprofile.school
    currentPeriod = request.user.userprofile.period

    context_dictionary['weekday'] = request.GET.get("weekday")
    if context_dictionary['weekday'] not in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        context_dictionary['weekday'] = datetime.datetime.today().strftime('%a')

    filteredClassIDs = Class.objects.filter(school_id=currentSchool, period_id=currentPeriod).values_list('id', flat=True)
    classSchedule = ClassSchedule.objects.filter(sch_class_id__in=filteredClassIDs)
    if context_dictionary['weekday'] == 'Mon':
        classSchedule = classSchedule.filter(monday=True)
    elif context_dictionary['weekday'] == 'Tue':
        classSchedule = classSchedule.filter(tuesday=True)
    elif context_dictionary['weekday'] == 'Wed':
        classSchedule = classSchedule.filter(wednesday=True)
    elif context_dictionary['weekday'] == 'Thu':
        classSchedule = classSchedule.filter(thursday=True)
    elif context_dictionary['weekday'] == 'Fri':
        classSchedule = classSchedule.filter(friday=True)
    elif context_dictionary['weekday'] == 'Sat':
        classSchedule = classSchedule.filter(saturday=True)
    elif context_dictionary['weekday'] == 'Sun':
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

    context_dictionary['schedule'] = []
    for i in range(0, len(classTimes)):
        context_dictionary['schedule'].append([classTimes[i][0].strftime('%H:%M'), classTimes[i][1].strftime('%H:%M'), courseNames[i], numStudents[i], numTeachers[i], classIDs[i]])

    return render_to_response("dashboard/classes_schedule_page.html",context_dictionary,RequestContext(request))

def view_reports(request):
    
    context_dictionary = {}
        
    return render_to_response("reports/view_reports.html",context_dictionary,RequestContext(request))

def assignment(request):
    
    context_dictionary = {}
        
    return render_to_response("school_components/assignment.html",context_dictionary,RequestContext(request))


#def statistics_page(request):
#    
#    context_dictionary = {}
#    
#    classes = Attendance.objects.values_list('classID', flat=True).distinct().order_by('classID')
#    
#    context_dictionary['statistics'] = classes
#    
#    return render_to_response("dashboard/statistics_page.html",context_dictionary,RequestContext(request))
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
#     context_dictionary = {}

#     viewFilter = request.GET.get("viewFilter")
#     presentStudents = 0
#     absentStudents = 0
#     if viewFilter == "all":
#       presentStudents = Attendance.objects.filter(status=1).count()
#       absentStudents = Attendance.objects.filter(status=0).count()
#     else:
#       presentStudents = Attendance.objects.filter(classID=viewFilter).filter(status=1).count()
#       absentStudents = Attendance.objects.filter(classID=viewFilter).filter(status=0).count()
        
#     context_dictionary['attendance'] = [['Present', presentStudents], ['Absent', absentStudents]]
        
#     return render_to_response("dashboard/attendance_page.html",context_dictionary,RequestContext(request))

# def grades_page(request):
#     context_dictionary = {}
        
#     fStudents = Grade.objects.filter(grade__range=(0,49)).count()
#     dStudents = Grade.objects.filter(grade__range=(50,54)).count()
#     cStudents = Grade.objects.filter(grade__range=(55,67)).count()
#     bStudents = Grade.objects.filter(grade__range=(68,79)).count()
#     aStudents = Grade.objects.filter(grade__range=(80,100)).count()

#     context_dictionary['grades'] = [['A', aStudents], ['B', bStudents], ['C', cStudents], ['D', dStudents], ['F', fStudents]]
        
#     return render_to_response("dashboard/grades_page.html",context_dictionary,RequestContext(request))

# def custom_statistic_page(request):
#     context_dictionary = {}

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
            
#         context_dictionary['customStat'] = [[[xAxis, xAxisValues], [yAxis, yAxisValues]], title, chartType]
        
#     return render_to_response("dashboard/custom_statistic_page.html",context_dictionary,RequestContext(request))

# def custom_statistic_created_page(request):
#     context_dictionary = {}

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

#     return render_to_response("dashboard/custom_statistic_created_page.html",context_dictionary,RequestContext(request))
