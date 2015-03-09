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

    #dashboard
    url(r'^statistics/','aplus.views.statistics_page',name='statistics_page'),
    url(r'^notifications/','aplus.views.notifications_page',name='notifications_page'),
    url(r'^notifications_settings/','aplus.views.notifications_settings_page',name='notifications_settings_page'),    
    url(r'^classes_schedule/','aplus.views.classes_schedule_page',name='classes_schedule_page'),

    url(r'^attendance/','dashboard.views.attendance_page',name='attendance_page'),
    url(r'^grades/','dashboard.views.grades_page',name='grades_page'),
                       
    #accounts
    #url(r'^createteacher/','accounts.views.create_teacher',name='create_teacher'),
    url(r'^login/', 'django.contrib.auth.views.login',name='login'),
    url(r'^createteacher/','accounts.views.create_teacher_page',name='create_teacher_page'),
    url(r'^account/', include('accounts.urls', namespace='account', app_name='accounts')),
    url(r'^teachers/','accounts.views.teacherstable_page',name='teacherstable_page'),
                   
    #messages
    url(r'^messages/','messages.views.send_email',name='send_email'),
    url(r'^sent_messages/','messages.views.sent_mail',name='sent_mail'),
    url(r'^class_grading/','school_components.views.classes_view.class_grading',name='class_grading'),
    url(r'^class_attendance/','school_components.views.classes_view.class_attendance',name='class_attendance'),
                       
    #reports

    # send to the school_components urls.py
    url(r'^school/', include('school_components.urls', namespace='school', app_name='school')),

)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
)
