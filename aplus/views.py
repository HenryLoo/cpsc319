from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from aplus.forms import SettingsForm
from accounts.utils import *

@login_required
def settings_page(request):
        request = process_user_info(request)
        context_dictionary = {}

        return render_to_response("settings_page.html",context_dictionary,RequestContext(request))

@login_required
def settings_edit(request):
        request = process_user_info(request)
        cd = {}
        settings_form = SettingsForm(instance=request.user)
        cd['settings_form'] = settings_form
        
        if request.method == 'POST':
                settings_form = SettingsForm(request.POST, instance=request.user)
                if settings_form.is_valid():
                        settings_form.save()
                        cd['succ'] = True
                cd['settings_form'] = settings_form
                
                        

        return render_to_response("settings_edit.html",cd,RequestContext(request))
