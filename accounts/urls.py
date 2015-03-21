from django.conf.urls import patterns, url
from accounts import views

urlpatterns = patterns('',
	# teachers
	#url(r'^teachers/$', 
	#	'accounts.views.teachers_view.teacher_list', 
	#	name='teacherlist'),
	#url(r'^teachers/(?P<teacher_id>\d+)/$', 
	#	'accounts.views.teachers_view.teacher_list', 
	#	name='teacherlist'),

    url(r'^login/$', 'accounts.views.login_view', name='login_page'),             
	
	url(r'^teachers/create/$', 'accounts.views.create_teacher_view', name='create_teacher'),
    
    url(r'^teachers/view/$', 'accounts.views.view_teachers_view', name='view_teachers'),
	
	url(r'^teachers/view/(?P<teacher_id>\d+)/$', 'accounts.views.view_teachers_view', name='view_teachers'),
        url(r'^teachers/view/(?P<teacher_id>\d+)/edit/$', 'accounts.views.edit_teacher_view', name='edit_teacher'),
                       
	url(r'^teachers/upload/$', 'accounts.views.upload_teachers_view', name='upload_teachers'),

    url(r'^admins/create/$','accounts.views.create_admin_view', name='create_admin'),
        
    url(r'^admins/view/$','accounts.views.view_admins_view',name='view_admins'),

	url(r'^admins/view/(?P<admin_id>\d+)/$', 'accounts.views.view_admins_view', name='view_admins'),
        url(r'^admins/view/(?P<admin_id>\d+)/edit/$', 'accounts.views.edit_admin_view', name='edit_admin'),
             
    url(r'^teachers/export/$', 'accounts.views.export_teachers_view', name='export_teachers'),
              
	# admins
	#url(r'^admins/$', 
	#	'accounts.views.admins_view.parent_list', 
	#	name='adminlist'),
	#url(r'^admins/(?P<admin_id>\d+)/$', 
	#	'accounts.views.admins_view.parent_list', 
	#	name='adminlist'),
	#url(r'^admins/create/$', 
	#	'accounts.views.admins_view.parent_create', 
	#	name='admincreate'),
	#url(r'^admins/form/$', 
	#	'accounts.views.admins_view.parent_form', 
	#	name='adminform'),
)
