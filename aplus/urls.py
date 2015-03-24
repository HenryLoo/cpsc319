from django.conf.urls import patterns, include, url
import os
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aplus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                 
                       
    url(r'^admin/', include(admin.site.urls)), #admin
                       
    url(r'^$', 'accounts.views.login_view', name='login_page'), #landing page = login

    
    url(r'^settings/edit/','aplus.views.settings_edit',name='settingsedit'),
    url(r'^settings/','aplus.views.settings_page',name='settings_page'), #settings
    #accounts
    url(r'^account/', include('accounts.urls', namespace='account', app_name='accounts')),

    #dashboard
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard', app_name='dashboard')),
   
                   
    #messages
    url(r'^messages/', include('messages.urls', namespace='messages', app_name='messages')),
               
    #reports
    url(r'^reports/', include('reports.urls', namespace='reports', app_name='reports')),
                       
    # send to the school_components urls.py
    url(r'^school/', include('school_components.urls', namespace='school', app_name='school')),
   
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
)
