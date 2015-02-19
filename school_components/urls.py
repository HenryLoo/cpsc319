from django.conf.urls import patterns, url
from school_components.views.students_view import *

urlpatterns = patterns('',
	url(r'^students/', StudentList.as_view(), name='studentlist'),
	url(r'^students/(?P<pk>\d+)/$', StudentDetailView.as_view(), name='studentdetail'),
)