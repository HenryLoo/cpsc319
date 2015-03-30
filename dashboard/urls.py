from django.conf.urls import patterns, url
from dashboard import views


urlpatterns = patterns('',

    url(r'^statistics/','dashboard.views.statistics_page',name='statistics_page'),
    url(r'^statistics_edit/','dashboard.views.statistics_edit_page',name='statistics_edit_page'),
    url(r'^notifications/','dashboard.views.notifications_page',name='notifications_page'),
    url(r'^notifications_settings/','dashboard.views.notifications_settings_page',name='notifications_settings_page'),
    url(r'^classes_schedule/','dashboard.views.classes_schedule_page',name='classes_schedule_page'),

)
