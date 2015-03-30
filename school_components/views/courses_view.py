from school_components.models.courses_model import Course, Prerequisite, Department
from school_components.forms.courses_form import *
from school_components.models.classes_model import Assignment, Class
from school_components.forms.classes_form import ClassAssignmentForm

from accounts.utils import *
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required

@login_required
def course_list(request, course_id=None):
	request = process_user_info(request)
	course_list = Course.objects.filter(
		school = request.user_school, 
		period = request.user_period
	).order_by('name')

	search_course = request.GET.get('course', None) 
	search_dept = request.GET.get('department', None)  
	
	if search_course:
		course_list = course_list.filter(
			name__icontains=search_course)

	if search_dept:
		course_list = course_list.filter(
			department__name__icontains=search_dept)


	context_dictionary = {'course_list': course_list, 'course_filter' : CourseFilter() }

	if course_id:
		try:
			c = Course.objects.get(pk=course_id)
			if c.school != request.user_school or c.period != request.user_period:
					raise ObjectDoesNotExist

			p = Prerequisite.objects.filter(course=course_id)
			context_dictionary['course'] = c
			if len(p) == 1:
					context_dictionary['prereq'] = p[0].prereq
		except ObjectDoesNotExist:
				context_dictionary['error'] = 'There is no course with that id in this school and period.'
						
	return render_to_response("courses/course_list.html",
		context_dictionary,
		RequestContext(request))

@login_required
def course_create(request):
	request = process_user_info(request)
	course_form = CourseForm()
	course_form.fields['prerequisite'].queryset = Course.objects.filter(
		school = request.user_school, 
		period = request.user_period
	)
	context_dictionary = { 'course_form': course_form }

	if request.method == 'POST':
		cf = CourseForm(request.POST)
		if cf.is_valid():
			new = cf.save(commit=False)
			new.school = request.user_school
			new.period = request.user_period
			new.save()

			if cf['prerequisite'].value() != '':
				prq = Course.objects.get(pk=cf['prerequisite'].value())
				p = Prerequisite(course=new, prereq=prq)
				p.save()

			return HttpResponseRedirect(
				reverse('school:courselist', args=(new.id,)))
		else:
			context_dictionary['errors'] = cf.errors 

	return render_to_response('courses/course_form.html',
		context_dictionary,
		RequestContext(request))

'''
Delete Course
'''
@login_required
def course_delete(request, course_id):
    request = process_user_info(request)
    course = Course.objects.get(pk=course_id)
    Prerequisite.objects.filter(Q(course=course) | Q(prereq=course)).delete()
    course.delete()

    messages.success(request, "Course has been deleted!")
    return redirect('school:courselist')

@login_required
def course_edit(request, course_id):
		request = process_user_info(request)
		course_list = Course.objects.filter(school = request.user_school, period = request.user_period).order_by('name')
		context_dictionary = {'course_list': course_list}

		try:
				c = Course.objects.get(pk=course_id)
				if c.school != request.user_school or c.period != request.user_period:
						raise ObjectDoesNotExist

				p = Prerequisite.objects.filter(course=course_id)

				if len(p) == 1:
					context_dictionary['prereq'] = p[0].prereq
			
				context_dictionary['course_id'] = course_id

				course_form = CourseForm(instance = c)
				
				if request.method == 'POST':
						course_form = CourseForm(request.POST, instance = c)
						if course_form.is_valid():
								course_form.save()
								context_dictionary['succ']=True
								
				context_dictionary['course_form'] = course_form
				
		except ObjectDoesNotExist:
				context_dictionary['error'] = 'There is no course in this school and period with that id.'
						
		return render_to_response("courses/course_edit.html", context_dictionary, RequestContext(request))

@login_required
def dept_create(request):
	request = process_user_info(request)
	context_dictionary = {'dept_form': DepartmentForm()}
	if request.method == 'POST':
		d = DepartmentForm(request.POST)
		if d.is_valid():
			new = d.save(commit=False)
			new.school = request.user_school
			new.save()
			return HttpResponseRedirect(reverse('school:courselist'))
		else:
			context_dictionary['errors'] = d.errors 

	return render_to_response('courses/dept_form.html',
		context_dictionary,
		RequestContext(request))

#create department view
@login_required
def dept_list(request, dept_id = None):
	request = process_user_info(request)
	dept_list = Department.objects.filter(school = request.user_school).order_by('name')

	search_dept = request.GET.get('department_name', None)  
	
	if search_dept:
		dept_list = dept_list.filter(name__icontains=search_dept)

	context_dictionary = {'dept_list': dept_list, 'dept_filter': DepartmentFilter() }

	if dept_id:
				try:
						d = Department.objects.get(pk=dept_id)
						if d.school != request.user_school:
								raise ObjectDoesNotExist
						context_dictionary['department'] = d
				except ObjectDoesNotExist:
						context_dictionary['error'] = 'There is no department in this school and period with that id.'
						
	return render_to_response("courses/dept_list.html",
		context_dictionary,
		RequestContext(request))

@login_required
def dept_edit(request, dept_id):
	request = process_user_info(request)
	dept_list = Department.objects.filter(school = request.user_school).order_by('name')
	context_dictionary = {'dept_list': dept_list}

	try:
				d = Department.objects.get(pk=dept_id)
				if d.school != request.user_school:
						raise ObjectDoesNotExist
				context_dictionary['dept_id'] = dept_id

				dept_form = DepartmentForm(instance = d)
				
				if request.method == 'POST':
						dept_form = DepartmentForm(request.POST, instance = d)
						if dept_form.is_valid():
								dept_form.save()
								context_dictionary['succ']=True
								
				context_dictionary['dept_form'] = dept_form
				
	except ObjectDoesNotExist:
				context_dictionary['error'] = 'There is no department in this school and period with that id.'
						
	return render_to_response("courses/dept_edit.html", context_dictionary, RequestContext(request))

'''
Delete Department
'''
@login_required
def dept_delete(request, dept_id):
    dep = Department.objects.get(pk=dept_id)
    #courses = Course.objects.filter(department=dep)
    #Prerequisite.objects.filter(Q(course__in=courses) | Q(prereq__in=courses)).delete()
    #courses.delete()

    dep.delete()
    messages.success(request, "Department has been deleted!")
    return redirect('school:deptlist')

@login_required
def course_assignment(request, course_id=None):
	request = process_user_info(request)

	course_list = Course.objects.filter(school = request.user_school, period = request.user_period).order_by('-id')
	context_dictionary = { 'course_list': course_list }

	if course_id:
		c = Course.objects.get(pk=course_id)
		context_dictionary['course'] = c

		assigments_list = Assignment.objects.filter(reg_class__course=c).order_by('-date')
		context_dictionary['assignments'] = assigments_list
	
	if request.method == 'POST':
		c = Course.objects.get(pk=course_id)
		classes = Class.objects.filter(course=c)
		for cl in classes:

			form = ClassAssignmentForm(request.POST, request.FILES)
			if form.is_valid():
				new = form.save(commit=False)
				this_class = Class.objects.get(pk=cl.id)
				new.reg_class = this_class
				new.content = request.FILES['content']
				new.save()
				# Redirect to the document list after POST
		
		return HttpResponseRedirect(
			reverse('school:courseassignment', args=(course_id,)))

	else:
		form = ClassAssignmentForm()

	context_dictionary['form'] = form


	return render_to_response('courses/course_assignment.html', context_dictionary,
		RequestContext(request))


