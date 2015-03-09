from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def statistics_page(request):

	context_dictionary = {}

	return render_to_response("dashboard/statistics_page.html",context_dictionary,RequestContext(request))

def notifications_page(request):

	context_dictionary = {}

	return render_to_response("dashboard/notifications_page.html",context_dictionary,RequestContext(request))

def classes_schedule_page(request):

	context_dictionary = {}

	return render_to_response("dashboard/classes_schedule_page.html",context_dictionary,RequestContext(request))

def view_reports(request):

	context_dictionary = {}

	return render_to_response("reports/view_reports.html",context_dictionary,RequestContext(request))

def view_assignment(request):

	context_dictionary = {}

	return render_to_response("school_components/view_assignment.html",context_dictionary,RequestContext(request))


