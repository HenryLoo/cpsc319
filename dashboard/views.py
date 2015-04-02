from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from accounts.utils import *

from dashboard.models import Chart, Notification, NotificationType
from dashboard.forms import ChartForm, NotificationsSettingsForm

from accounts.models import UserProfile

from school_components.models import Class, ClassAttendance, ClassSchedule, ClassRegistration, ClassTeacher, Course, Grading, Parent, Payment, Period, School, Student

from django.db.models import Q

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import Avg, Sum, Count
from django.forms.models import model_to_dict
from django.forms.models import modelformset_factory

import datetime

from operator import attrgetter
from itertools import chain, groupby

from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required

from graphos.sources.model import SimpleDataSource
from graphos.renderers import gchart

@login_required
def statistics_page(request):
    request = process_user_info(request)
    context_dictionary = {}

    currentSchool = request.user_school
    currentPeriod = request.user_period

    chartForm = ChartForm(request.POST)
    context_dictionary['chartForm'] = ChartForm()
    if request.method == 'POST':        
        if chartForm.is_valid():
          chartEntry = chartForm.save(commit=False)
          chartEntry.school = currentSchool
          chartEntry.period = currentPeriod
          chartEntry.save()
          context_dictionary['success'] = 'New custom statistic successfully added.'
        else:
        	context_dictionary['error'] = 'Error: Please check the form field values.'

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
    context_dictionary['payments'] = [paymentTotal, receipts]

    regXAxis = Period.objects.filter(school_id=currentSchool).all().order_by('start_date').values_list('description', flat=True)
    regYAxis = ClassRegistration.objects.filter(school_id=currentSchool).values_list('student_id', 'period_id').distinct().values('period_id').annotate(num_students=Count('period')).values_list('num_students', flat=True)
    regData = [['School', 'Students']]
    for x in zip(regXAxis, regYAxis):
        regData.append([x[0], x[1]])
    regDataSource = SimpleDataSource(regData)
    context_dictionary['registrationChart'] = gchart.LineChart(regDataSource, options={'title': "Student Registration", 'width': 299, 'height': 299})

    
    performance = Grading.objects.filter(reg_class__school=currentSchool, reg_class__period=currentPeriod).values('student_id').annotate(avg_grades=Avg('performance'))
    gradeList = [round(grade) for grade in performance.order_by('avg_grades').values_list('avg_grades', flat=True)]
    performXAxis = list(set(gradeList))
    performYAxis = [len(list(group)) for key, group in groupby(gradeList)]
    performData = [['Grades', 'Students']]
    for x in zip(performXAxis, performYAxis):
        performData.append([x[0], x[1]])
    performDataSource = SimpleDataSource(performData)
    context_dictionary['performanceChart'] = gchart.LineChart(performDataSource, options={'title': "Student Performance", 'width': 299, 'height': 299})

    numPass = sum(grade >= 50 for grade in gradeList)
    numFail = sum(grade < 50 for grade in gradeList)
    passFailDataSource = SimpleDataSource([['Status', 'Students'], ['Pass', numPass], ['Fail', numFail]])
    context_dictionary['passFailChart'] = gchart.PieChart(passFailDataSource, options={'title': "Passing/Failing Students", 'width': 299, 'height': 299})

    charts = Chart.objects.filter(school_id=currentSchool, period_id=currentPeriod)
    if request.user_role == 'TEACHER':
        charts = charts.filter(visibility='ALL')
    charts = charts.all().order_by('id')

    allChartData = []
    for chart in charts:
        xAxis = ''
        xIDs = ''
        xFilter = ''
        xLabel = ''
        if chart.x_axis == 'SCHOOL':
            schools = School.objects.all()
            xAxis = schools.values_list('title', flat=True)
            xIDs = schools.values_list('id', flat=True)
            xFilter = 'school_id'
            xLabel = 'Schools'
        elif chart.x_axis == 'PERIOD':
            periods = Period.objects.filter(school=currentSchool).all()
            xAxis = periods.values_list('description', flat=True)
            xIDs = periods.values_list('id', flat=True)
            xFilter = 'period_id'
            xLabel = 'Periods'
        elif chart.x_axis == 'COURSE':
            courses = Course.objects.filter(school=currentSchool, period=currentPeriod)
            xAxis = courses.values_list('name', flat=True)
            xIDs = courses.values_list('id', flat=True)
            xFilter = 'course_id'
            xLabel = 'Courses'

        yAxis = []
        yLabel = ''
        classes = Class.objects
        for x in xIDs:
            filteredClassIDs = classes.filter(**{xFilter: x}).values_list('id', flat=True)
            if chart.y_axis == 'NSTUDENTS':
                yAxis.append(ClassRegistration.objects.filter(reg_class_id__in=filteredClassIDs).all().values('student_id').distinct().count())
                yLabel = 'Students'
            elif chart.y_axis == 'NCLASSES':
                yAxis.append(len(filteredClassIDs))
                yLabel = 'Classes'
            elif chart.y_axis == 'NTEACHERS':
                primaryTeachers = ClassTeacher.objects.filter(primary_teacher_id__in=filteredClassIDs).all().values('primary_teacher_id').distinct()
                secondaryTeachers = ClassTeacher.objects.filter(secondary_teacher_id__in=filteredClassIDs).all().values('secondary_teacher_id').distinct()
                numTeachers = len(list(set(list(chain(primaryTeachers, secondaryTeachers)))))
                yAxis.append(numTeachers)
                yLabel = 'Teachers'
            elif chart.y_axis == 'ATTENDANCE':
                allAttendance = ClassAttendance.objects.filter(reg_class_id__in=filteredClassIDs)
                numAttended = allAttendance.exclude(attendance='A').all().count()
                numTotal = allAttendance.all().count()
                if numTotal == 0:
                    numTotal = 1
                yAxis.append(round(numAttended/numTotal))
                yLabel = 'Attendance Rates (%)'
            elif chart.y_axis == 'PERFORMANCE':
                averages = Grading.objects.filter(reg_class_id__in=filteredClassIDs).annotate(avg_grades=Avg('performance')).values_list('avg_grades', flat=True)
                numGrades = len(averages)
                if numGrades == 0:
                    numGrades = 1;
                yAxis.append(round(sum(averages)/numGrades))
                yLabel = 'Average Grades (%)'

        chartData = [[xLabel, yLabel]]
        for x in zip(xAxis, yAxis):
            chartData.append([x[0], x[1]])
        allChartData.append(chartData)

    chartsWithData = []
    for x in zip(charts, allChartData):
        chartTypeField = x[0].chart_type
        chart = ''
        chartDataSource = SimpleDataSource(x[1])
        if chartTypeField == 'BAR':
            chart = gchart.BarChart(chartDataSource, options={'title': x[0].title, 'width': 299, 'height': 299})
        elif chartTypeField == 'PIE':
            chart = gchart.PieChart(chartDataSource, options={'title': x[0].title, 'width': 299, 'height': 299})
        elif chartTypeField == 'LINE':
            chart = gchart.LineChart(chartDataSource, options={'title': x[0].title, 'width': 299, 'height': 299})
        chartsWithData.append([x[0], chart])

    context_dictionary['customChartsTriplets'] = []
    for i in range(0, len(chartsWithData), 3):
        context_dictionary['customChartsTriplets'].append(chartsWithData[i:i+3])


    return render_to_response("dashboard/statistics_page.html",context_dictionary,RequestContext(request))

@login_required
def statistics_edit_page(request):
    request = process_user_info(request)
    context_dictionary = {}

    currentSchool = request.user_school
    currentPeriod = request.user_period

    chartID = request.GET.get("chart")
    if chartID == '':
    	context_dictionary['error'] = 'Error: This chart does not exist.'
    else:
        try:
            chart = Chart.objects.get(pk=chartID)
            context_dictionary['chart'] = chart
            chartForm = ChartForm(request.POST, instance=chart)

            context_dictionary['chartForm'] = ChartForm(instance=chart)
            if request.method == 'POST':
                if chartForm.is_valid():
                    chartEntry = chartForm.save(commit=False)
                    chartEntry.school = currentSchool
                    chartEntry.period = currentPeriod
                    chartEntry.save()
                    context_dictionary['success'] = 'Changes have been successfully saved.'
                    context_dictionary['chartForm'] = ChartForm(instance=chart)
                else:
                    context_dictionary['error'] = 'Error: Please check the form field values.'
        except ObjectDoesNotExist:
            context_dictionary['error'] = 'Error: This chart does not exist.'

    return render_to_response("dashboard/statistics_edit_page.html",context_dictionary,RequestContext(request))

@login_required
def notifications_page(request):
    request = process_user_info(request)
    
    context_dictionary = {}

    currentSchool = request.user_school
    currentPeriod = request.user_period

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
        
    return render_to_response("dashboard/notifications_page.html",context_dictionary,RequestContext(request))

@login_required
def notifications_settings_page(request):
    request = process_user_info(request)
    
    context_dictionary = {}

    try:
    	attendance = NotificationType.objects.get(notification_type='Attendance')
    except ObjectDoesNotExist:
    	attendance = NotificationType(notification_type='Attendance', condition=3, content='Student missed 3 classes in a row.')
    	attendance.save()

    try:
    	performance = NotificationType.objects.get(notification_type='Performance')
    except ObjectDoesNotExist:
    	performance = NotificationType(notification_type='Performance', condition=50, content='Student is scoring lower than 50%% average.')
    	performance.save()

    try:
    	assignment = NotificationType.objects.get(notification_type='Assignment')
    except ObjectDoesNotExist:
    	assignment = NotificationType(notification_type='Assignment', condition=3, content='Student missed 3 assignments.')
    	assignment.save()
    
    NotifFormSet = modelformset_factory(NotificationType, form=NotificationsSettingsForm)
    queryset = NotificationType.objects.extra(
    	select={'ordering': "CASE WHEN notification_type='Attendance' THEN 1 WHEN notification_type='Performance' THEN 2 WHEN notification_type='Assignment' THEN 3 END"},
    	order_by=['ordering']
		)
    formset = NotifFormSet(queryset = queryset)
    if request.method == 'POST':
      formset = NotifFormSet(request.POST)
      if formset.is_valid():
        formset.save()
        context_dictionary['success'] = 'Notification settings updated.'
      else:
      	context_dictionary['error'] = 'Error: Please check the form field values.'

    context_dictionary['formset'] = formset

    return render_to_response("dashboard/notifications_settings_page.html",context_dictionary,RequestContext(request))

@login_required
def classes_schedule_page(request):
    request = process_user_info(request)
    
    context_dictionary = {}

    currentSchool = request.user_school
    currentPeriod = request.user_period

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

    if request.user_role == 'TEACHER':
        teacherID = request.user_profile.teachers.all()[0].id
        taughtClassesPrimary = ClassTeacher.objects.filter(primary_teacher_id=teacherID).values_list('taught_class_id', flat=True)
        taughtClassesSecondary = ClassTeacher.objects.filter(secondary_teacher_id=teacherID).values_list('taught_class_id', flat=True)
        taughtClasses = list(set(list(chain(taughtClassesPrimary, taughtClassesSecondary))))
        classSchedule = classSchedule.filter(sch_class_id__in=taughtClasses)
    
    classTimes = classSchedule.values_list('start_time', 'end_time')
    courseIDs = []
    numStudents = []
    numTeachers = []
    classIDs = classSchedule.values_list('sch_class_id', flat=True)
    for x in classIDs:
        courseIDs.append(Class.objects.get(pk=x).course_id)
        numStudents.append(ClassRegistration.objects.filter(reg_class_id=x).count())
        numTeachers.append(ClassTeacher.objects.filter(taught_class_id=x).count() + ClassTeacher.objects.filter(taught_class_id=x, secondary_teacher_id__isnull=False).count())

    courseNames = []
    for x in courseIDs:
        courseNames.append(Course.objects.get(pk=x).name)

    context_dictionary['schedule'] = []
    for i in range(0, len(classTimes)):
        context_dictionary['schedule'].append([classTimes[i][0].strftime('%H:%M'), classTimes[i][1].strftime('%H:%M'), courseNames[i], numStudents[i], numTeachers[i], classIDs[i]])

    return render_to_response("dashboard/classes_schedule_page.html",context_dictionary,RequestContext(request))

@login_required
def view_reports(request):
    request = process_user_info(request)
    
    context_dictionary = {}
        
    return render_to_response("reports/view_reports.html",context_dictionary,RequestContext(request))

@login_required
def assignment(request):
    request = process_user_info(request)
    
    context_dictionary = {}
        
    return render_to_response("school_components/assignment.html",context_dictionary,RequestContext(request))
