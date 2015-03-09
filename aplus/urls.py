from django.conf.urls import patterns, include, url
import os
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aplus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'accounts.views.login_view', name='login_page'),  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^settings/','aplus.views.settings_page',name='settings_page'),
    #dashboard
    url(r'^statistics/','aplus.views.statistics_page',name='statistics_page'),
    url(r'^statisticsdemo/','aplus.views.demostatistics_page',name='demostatistics_page'),
    url(r'^notifications/','aplus.views.notifications_page',name='notifications_page'),
    url(r'^notifications_settings/','aplus.views.notifications_settings_page',name='notifications_settings_page'),    
    url(r'^classes_schedule/','aplus.views.classes_schedule_page',name='classes_schedule_page'),

    url(r'^attendance/','dashboard.views.attendance_page',name='attendance_page'),
    url(r'^grades/','dashboard.views.grades_page',name='grades_page'),
    url(r'^customstat/','dashboard.views.custom_statistic_page',name='custom_statistic_page'),

                       
    #accounts
    url(r'^account/', include('accounts.urls', namespace='account', app_name='accounts')),

                   
    #messages
    url(r'^messages/','messages.views.send_email',name='send_email'),
    url(r'^sent_messages/','messages.views.sent_mail',name='sent_mail'),
               
    #reports
    url(r'^view_reports/','reports.views.view_reports',name='view_reports'),
    url(r'^create_new_report_page/','reports.views.create_new_report_page',name='create_new_report_page'),
                       
    # send to the school_components urls.py
    url(r'^school/', include('school_components.urls', namespace='school', app_name='school')),




                  
   
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
)
