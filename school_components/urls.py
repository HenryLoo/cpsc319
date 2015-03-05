from django.conf.urls import patterns, url
from school_components import views

urlpatterns = patterns('',
	# students
	url(r'^students/$', 
		'school_components.views.students_view.student_list', 
		name='studentlist'),
	url(r'^students/(?P<student_id>\d+)/$', 
		'school_components.views.students_view.student_detail', 
		name='studentdetail'),
	url(r'^students/create/$', 
		'school_components.views.students_view.student_create', 
		name='studentcreate'),
	url(r'^students/form/$', 
		'school_components.views.students_view.student_form', 
		name='studentform'),
	url(r'^students/upload/$', 
		'school_components.views.students_view.student_upload', 
		name='studentupload'),
	url(r'^students/export/$', 
		'school_components.views.students_view.student_export', 
		name='studentexport'),

	# parents
	url(r'^parents/$', 
		'school_components.views.parents_view.parent_list', 
		name='parentlist'),
	url(r'^parents/(?P<parent_id>\d+)/$', 
		'school_components.views.parents_view.parent_detail', 
		name='parentdetail'),
	url(r'^parents/create/$', 
		'school_components.views.parents_view.parent_create', 
		name='parentcreate'),
	url(r'^parents/form/$', 
		'school_components.views.parents_view.parent_form', 
		name='parentform'),
)