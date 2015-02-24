from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.mail import EmailMessage
from messages.forms import EmailForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_email(request):
  if request.method != 'POST':
    form = EmailForm()
    return render_to_response('messages/messages_page.html', {'email_form': form})

    form = EmailForm(request.POST, request.FILES)
    if form.is_valid():
      subject = form.cleaned_data['subject']
      message = form.cleaned_data['message']
      email = form.cleaned_data['email']
      attach = request.FILES['attach']
  else:
    form = EmailForm()
    try:
      mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
      mail.attach(attach.name, attach.read(), attach.content_type)
      mail.send()
      return render_to_response('messages/messages_page.html', {'message': 'Sent email to %s'%email})
    except:#(ValueError, TypeError, AttributeError, KeyError):
      return render_to_response('404.html', {'message': 'Either the attachment is too  big or corrupt'})
    return render_to_response('messages/messages_page.html', {'message': 'Unable to send email. Please try again later'})
	# context_dictionary = {}

	# return render_to_response("messages/messages_page.html",context_dictionary,RequestContext(request))