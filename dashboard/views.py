from django.shortcuts import render
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from dashboard.models import Attendance
from dashboard.models import Grade

from django.db.models import Q


def statistics_page(request):
    
    return_dict = {}
    
    classes = Attendance.objects.values_list('classID', flat=True).distinct().order_by('classID')
    
    return_dict['statistics'] = classes
    
    return render_to_response("dashboard/statistics_page.html",return_dict,RequestContext(request))

def notifications_page(request):
    
    context_dictionary = {}
        
    return render_to_response("dashboard/notifications_page.html",context_dictionary,RequestContext(request))

def classes_schedule_page(request):
    
    context_dictionary = {}
        
    return render_to_response("dashboard/classes_schedule_page.html",context_dictionary,RequestContext(request))

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

    title = request.GET.get("title")
    hAxis = request.GET.get("hAxis")
    vAxis = request.GET.get("vAxis")
    chartType = request.GET.get("chartType")
    visibility = request.GET.get("visibility")

    hAxisValues = 0
    vAxisValues = 0
    if hAxis == "Attended":
    	hAxisValues = Attendance.objects.filter(status=1).count()
    elif hAxis == "Absences":
    	hAxisValues = Attendance.objects.filter(status=0).count()
    elif hAxis == "Grades":
    	hAxisValues = Grade.objects.filter(grade__range=(0,100))

    if vAxis == "Attended":
    	vAxisValues = Attendance.objects.filter(status=1).count()
    elif vAxis == "Absences":
    	vAxisValues = Attendance.objects.filter(status=0).count()
    elif vAxis == "Grades":
    	vAxisValues = Grade.objects.filter(grade__range=(0,100))
        
    return_dict['customStat'] = [[[hAxis, hAxisValues], [vAxis, vAxisValues]], title, chartType, visibility]
        
    return render_to_response("dashboard/custom_statistic_page.html",return_dict,RequestContext(request))

