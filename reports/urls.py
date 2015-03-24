from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
   
    #reports
    url(r'^view_reports/','reports.views.view_reports',name='view_reports'),

    url(r'^search_st/','reports.views.search_st',name='search_st'),

    url(r'^class_list/','reports.views.class_list',name='class_list'),

    url(r'^find_section/','reports.views.find_section',name='find_section'),

    url(r'^search_attendance/','reports.views.search_attendance',name='search_attendance'),
)
