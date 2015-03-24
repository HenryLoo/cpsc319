from school_components.models.courses_model import Course, Prerequisite, Department
from school_components.forms.courses_form import CourseForm, DepartmentForm
from school_components.models.classes_model import Assignment, Class
from school_components.forms.classes_form import ClassAssignmentForm

from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist


def course_list(request, course_id=None):
	course_list = Course.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('name')
	context_dictionary = {'course_list': course_list}

	if course_id:
		c = Course.objects.get(pk=course_id)
		context_dictionary['course'] = c
		p = Prerequisite.objects.filter(course=course_id)
		if len(p) == 1:
			context_dictionary['prereq'] = p[0].prereq
	return render_to_response("courses/course_list.html",
		context_dictionary,
		RequestContext(request))

def course_create(request):
	context_dictionary = { 'course_form': CourseForm() }
	if request.method == 'POST':
		cf = CourseForm(request.POST)
		if cf.is_valid():
			new = cf.save(commit=False)
			new.school = request.user.userprofile.school
			new.period = request.user.userprofile.period
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


def dept_create(request):
	context_dictionary = {'dept_form': DepartmentForm()}
	if request.method == 'POST':
		d = DepartmentForm(request.POST)
		if d.is_valid():
			new = d.save(commit=False)
			new.school = request.user.userprofile.school
			new.save()
			return HttpResponseRedirect(reverse('school:courselist'))
		else:
			context_dictionary['errors'] = d.errors 

	return render_to_response('courses/dept_form.html',
		context_dictionary,
		RequestContext(request))

#create department view

def dept_list(request, dept_id = None):
        dept_list = Department.objects.filter(school = request.user.userprofile.school).order_by('name')
	context_dictionary = {'dept_list': dept_list}

	if dept_id:
                try:
                        d = Department.objects.get(pk=dept_id)
                        if d.school != request.user.userprofile.school:
                                raise ObjectDoesNotExist
                        context_dictionary['department'] = d
                except ObjectDoesNotExist:
                        context_dictionary['error'] = 'There is no department in this school and period with that id.'
                        
	return render_to_response("courses/dept_list.html",
		context_dictionary,
		RequestContext(request))

def dept_edit(request, dept_id):
        dept_list = Department.objects.filter(school = request.user.userprofile.school).order_by('name')
	context_dictionary = {'dept_list': dept_list}

        try:
                d = Department.objects.get(pk=dept_id)
                if d.school != request.user.userprofile.school:
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
                        
	return render_to_response("courses/dept_edit.html",
		context_dictionary,
		RequestContext(request))


def course_assignment(request, course_id=None):

	course_list = Course.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('-id')
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


