
from school_components.models.classes_model import *
from school_components.models.students_model import Student
from school_components.forms.classes_form import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory

from django.forms.models import modelformset_factory

def class_list(request, class_id=None):
	class_list = Class.objects.filter(
		school = request.user.userprofile.school, 
		period = request.user.userprofile.period
	).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c
	
	return render_to_response("classes/class_list.html",
		context_dictionary,
		RequestContext(request))

def class_create(request):
	class_form = ClassForm(prefix='info')
	class_form.fields['course'].queryset = Course.objects.filter(
		school = request.user.userprofile.school, 
		period = request.user.userprofile.period
	)

	# TODO: teacher will have period field
	teacher_form = ClassTeacherForm(prefix='te')
	teacher_form.fields['teacher'].queryset = TeacherUser.objects.filter(
		user__period = request.user.userprofile.period, 
		user__school = request.user.userprofile.school
	)
   
	context_dictionary = {
		'class_form': class_form, 
		'classday_form': ClassScheduleForm(prefix='sch'),
		'classteacher_form': teacher_form
	}

	if request.method == 'POST':
		cf = ClassForm(request.POST, prefix='info')
		sf = ClassScheduleForm(request.POST, prefix='sch')

		if cf.is_valid() and sf.is_valid():
			# save class
			new = cf.save(commit=False)
			new.school = request.user.userprofile.school
			new.period = request.user.userprofile.period
			new.save()

			# save class schedule
			schedule = sf.save(commit=False)
			schedule.sch_class = new
			schedule.save()

			# save class teacher
			try:
				te = ClassTeacherForm(request.POST, prefix='te')
				if te.is_valid():
					teacher = te.save(commit=False)
					teacher.taught_class = new
					teacher.save()
			except Exception as e:
				# no teacher in request, don't create ClassTeacher object
				pass

			return HttpResponseRedirect(
				reverse('school:classlist', args=(new.id,)))
		else:
			context_dictionary['class_errors'] = cf.errors
			context_dictionary['schedule_errors'] = sf.errors
			context_dictionary['teacher_errors'] = te.errors

	return render_to_response('classes/class_form.html',
		context_dictionary,
		RequestContext(request))

def class_registration(request, class_id=None):
	if request.POST:
		return class_registration_helper(request, class_id)

	else:
		class_list = Class.objects.filter(
			school = request.user.userprofile.school, 
			period = request.user.userprofile.period).order_by('course')
		context_dictionary = {'class_list': class_list }

		if class_id:
			cl = Class.objects.get(pk=class_id)
			context_dictionary['class'] = cl 
			context_dictionary['student_list'] = Student.objects.filter(
				school = request.user.userprofile.school
			)
			context_dictionary['form'] = ClassRegistrationForm()
			context_dictionary['remove_form'] = RemoveClassRegistrationForm()
		
		return render_to_response("classes/class_registration.html",
			context_dictionary,
			RequestContext(request))

# register student to class
def class_registration_helper(request, class_id):
	student_id = request.POST['student_id']
	student = Student.objects.get(pk=student_idq)
	
	# check if on waiting list
	reg = student.enrolled_student.filter(reg_class__id=class_id)
	if len(reg) > 0:
		class_reg = reg[0]
		class_reg.registration_status = True
		class_reg.save()
		return HttpResponse("Successfully registered.")

	try:
		reg_class = Class.objects.get(pk=class_id)
		school = request.user.userprofile.school
		period = request.user.userprofile.period
		cr = ClassRegistration(
			reg_class=reg_class, student=student, school=school, 
			period=period, registration_status=True)

		cr.save()
		return HttpResponse("Successfully registered.")
	except IntegrityError:
		return HttpResponse("This student is already registered.")
	
	except Exception as e:
		return HttpResponseBadRequest(e)

# delete student from class
def class_remove_registration(request, class_id):
	try:
		student_id = request.POST['student_id']
		student = Student.objects.get(pk=student_id)
		reg_class = Class.objects.get(pk=class_id)
		cr = ClassRegistration.objects.filter(
			student=student).filter(reg_class=reg_class)
		cr.delete()
		return HttpResponse("Successfully removed from course.")
	
	except Exception as e:
		return HttpResponseBadRequest(e)


def class_attendance(request, class_id=None):
	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c

		class_reg_list = ClassRegistration.objects.filter(reg_class__id = class_id).order_by('student__first_name')
		context_dictionary['classregistration'] = class_reg_list

		AttendanceFormSetFactory = modelformset_factory(ClassAttendance, extra=0, can_delete=True)
		date_form = ClassAttendanceDateForm()
		context_dictionary['dateform'] = date_form

		if request.method == "POST":

				if '_date' in request.POST:

					date_form = ClassAttendanceDateForm(request.POST)
					inter = date_form['date'].value()
					if '/' in inter:
						x,y,z = inter.split('/')
						date_value = z + "-" + x + "-" + y
					else:
						date_value = inter	

					context_dictionary['date_value'] = date_value

					for cl in class_reg_list:
						verify = ClassAttendance.objects.filter(student=cl.student, reg_class=c, date=date_value)
						if len(verify) == 0:
							ClassAttendance.objects.create(student =cl.student, reg_class=c, date=date_value)

					formset = AttendanceFormSetFactory(queryset=ClassAttendance.objects.filter(date=date_value))
					context_dictionary['formset'] = formset

					date_form = ClassAttendanceDateForm(initial={'date': date_value})
					context_dictionary['dateform'] = date_form

					return render_to_response('classes/class_attendance.html', context_dictionary,
						RequestContext(request))

				elif '_attendance' in request.POST:

					date_form = ClassAttendanceDateForm(request.POST)
					date_value = date_form['date'].value()
					formset = AttendanceFormSetFactory(request.POST, queryset=ClassAttendance.objects.filter(date=date_value))

					if formset.is_valid():

						instances = formset.save(commit=False)
						for instance in instances:
							instance.reg_class = c
							instance.date = date_value
							instance.save()

					else:
						context_dictionary['errors'] = formset.errors

					context_dictionary['date_value'] = date_value

					formset = AttendanceFormSetFactory(queryset=ClassAttendance.objects.filter(date=date_value))
					context_dictionary['formset'] = formset

					date_form = ClassAttendanceDateForm(initial={'date': date_value})
					context_dictionary['dateform'] = date_form

					return render_to_response('classes/class_attendance.html', context_dictionary,
						RequestContext(request))

		else:
				date_form = ClassAttendanceDateForm()
				inter = date_form['date'].value()
				if inter and '/' in inter:
					x,y,z = inter.split('/')
					date_value = z + "-" + x + "-" + y
				else:
					date_value = inter	
				formset = AttendanceFormSetFactory(queryset=ClassAttendance.objects.filter(date=date_value))
		
		context_dictionary['dateform'] = date_form
		context_dictionary['formset'] = formset

	return render_to_response('classes/class_attendance.html', context_dictionary,
		RequestContext(request))

def class_performance(request, class_id=None, assignment_id=None):

	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c
		
		class_reg_list = ClassRegistration.objects.filter(reg_class__id = class_id).order_by('student__first_name')
		context_dictionary['classregistration'] = class_reg_list
	
		assigments_list = Assignment.objects.filter(reg_class=c).order_by('-date')
		context_dictionary['assignment_list'] = assigments_list

		if assignment_id:
			a = Assignment.objects.get(pk=assignment_id)
			for cl in class_reg_list:
				verify = Grading.objects.filter(student=cl.student, reg_class=c, assignment=a)
				if len(verify) == 0:
					Grading.objects.create(student =cl.student, reg_class=c, assignment=a)
			context_dictionary['assignment'] = a

			GradingFormSetFactory = inlineformset_factory(Assignment, Grading, extra=0, can_delete=True)
			assignment = Assignment.objects.get(pk=assignment_id)

			if request.method == "POST":

				formset = GradingFormSetFactory(request.POST, instance=assignment)

				if formset.is_valid():

					instances = formset.save(commit=False)
					for instance in instances:
						instance.assignment = a
						instance.reg_class = c
						instance.save()

					#performance
					for cl in class_reg_list:
						current = Grading.objects.get(student=cl.student, reg_class=c, assignment=a)
						grade = current.grade

						if grade == None:
							grade = 0.0
						total = a.total_weight
						current.performance = (grade/total) * 100
						current.save()


				else:
					print('Error')
					context_dictionary['errors'] = formset.errors
					print(formset.errors)

				return HttpResponseRedirect(
						reverse('school:classperformance', args=(class_id, assignment_id)))

			else:
				formset = GradingFormSetFactory(instance=assignment)
				
			context_dictionary['formset'] = formset

	return render_to_response('classes/class_grading.html', context_dictionary,
		RequestContext(request))


def class_assignment(request, class_id=None):
	
	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c

		assigments_list = Assignment.objects.filter(reg_class=c).order_by('-date')
		context_dictionary['assignments'] = assigments_list
	
	if request.method == 'POST':
		form = ClassAssignmentForm(request.POST, request.FILES)
		if form.is_valid():
			new = form.save(commit=False)
			c = Class.objects.get(pk=class_id)
			new.reg_class = c
			new.content = request.FILES['content']
			new.save()
            # Redirect to the document list after POST
			return HttpResponseRedirect(
				reverse('school:classassignment', args=(class_id,)))
	else:
		form = ClassAssignmentForm()

	context_dictionary['form'] = form


	return render_to_response('classes/class_assignment.html', context_dictionary,
		RequestContext(request))

def class_reportcard(request, class_id=None, student_id=None):
	class_list = Class.objects.filter(school = request.user.userprofile.school, period = request.user.userprofile.period).order_by('course')
	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c

	if student_id:
		s = Student.objects.get(pk=student_id)
		context_dictionary['student'] = s

		grading_list = Grading.objects.filter(student=s, reg_class=c).order_by('-assignment__date').reverse()
		context_dictionary['gradinglist'] = grading_list

		cont=0
		for g in grading_list:
			cont = cont + g.performance
		total = len(grading_list)
		average = cont/total
		context_dictionary['overall'] = average

	return render_to_response('classes/class_reportcard.html', context_dictionary,
		RequestContext(request))
