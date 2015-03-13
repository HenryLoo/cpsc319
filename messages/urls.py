from django.conf.urls import patterns, url
from messages import views

urlpatterns = patterns('',

                       
    url(r'^messages/','messages.views.send_email',name='send_email'),
    url(r'^sent_messages/','messages.views.sent_mail',name='sent_mail'),
               
)