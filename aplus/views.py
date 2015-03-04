from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from dashboard.models import Attendance

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