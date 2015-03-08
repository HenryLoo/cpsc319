from django.conf.urls import patterns, include, url
import os
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aplus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

	url(r'^$','aplus.views.statistics_page',name='statistics_page'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^statistics/','aplus.views.statistics_page',name='statistics_page'),
    url(r'^notifications/','aplus.views.notifications_page',name='notifications_page'),    
    url(r'^classes_schedule/','aplus.views.classes_schedule_page',name='classes_schedule_page'),

    url(r'^teachers/','accounts.views.teacherstable_page',name='teacherstable_page'),

    url(r'^createteacher/','accounts.views.create_teacher_page',name='create_teacher_page'),

    url(r'^view_reports/','reports.views.view_reports',name='view_reports'),

    url(r'^create_new_report_page/','reports.views.create_new_report_page',name='create_new_report_page'),

                  
   
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
)
