from django.conf.urls import patterns, url
from dashboard import views


urlpatterns = patterns('',

    url(r'^statistics/','dashboard.views.statistics_page',name='statistics_page'),
    url(r'^statisticsdemo/','dashboard.views.demostatistics_page',name='demostatistics_page'),
    url(r'^notifications/','dashboard.views.notifications_page',name='notifications_page'),
    url(r'^notifications_settings/','dashboard.views.notifications_settings_page',name='notifications_settings_page'),
    url(r'^classes_schedule/','dashboard.views.classes_schedule_page',name='classes_schedule_page'),

    url(r'^attendance/','dashboard.views.attendance_page',name='attendance_page'),
    url(r'^grades/','dashboard.views.grades_page',name='grades_page'),
    url(r'^customstat/','dashboard.views.custom_statistic_page',name='custom_statistic_page'),
    url(r'^customstatcreated/','dashboard.views.custom_statistic_created_page',name='custom_statistic_created_page'),

)
