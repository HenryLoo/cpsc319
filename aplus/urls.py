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

<<<<<<< HEAD
#    url(r'^teachers/','accounts.views.teacherstable_page',name='teacherstable_page'),

    url(r'^createteacher/','accounts.views.create_teacher',name='create_teacher'),
    url(r'^login/', 'django.contrib.auth.views.login',name='login')

=======
    url(r'^teachers/','accounts.views.teacherstable_page',name='teacherstable_page'),
    url(r'^createteacher/','accounts.views.create_teacher_page',name='create_teacher_page'),

    # send to the school_components urls.py
    url(r'^school/', include('school_components.urls', 
        namespace='school', app_name='school')),
>>>>>>> flora
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
)
