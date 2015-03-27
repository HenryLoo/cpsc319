from django.conf.urls import patterns, url
from aplusmessages import views

urlpatterns = patterns('',

                       
    url(r'^messages/', 'aplusmessages.views.send_email',name='send_email'),
    url(r'^sent_messages/', 'aplusmessages.views.sent_mail',name='sent_mail'),
               
)