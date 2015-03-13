from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def settings_page(request):

	context_dictionary = {}

	return render_to_response("settings_page.html",context_dictionary,RequestContext(request))
