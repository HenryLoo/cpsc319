from django.conf.urls import patterns, url
from reports import views

urlpatterns = patterns('',
   
    #reports
    url(r'^view_reports/','reports.views.view_reports',name='view_reports'),
    url(r'^create_new_report_page/','reports.views.create_new_report_page',name='create_new_report_page'),
                       
   
)
