
from school_components.models.classes_model import *
from school_components.models.students_model import Student
from school_components.forms.classes_form import *
from accounts.models import TeacherUser
from accounts.utils import *
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from datetime import datetime
from dashboard.models import *
from django.contrib import messages
from django.shortcuts import redirect

from django.forms.models import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.contrib.auth.decorators import login_required


@login_required
def class_list(request, class_id=None):

	request = process_user_info(request)
        
	if request.user_role == 'TEACHER':
		teacherID = request.user_profile.teachers.first().id
		# class_teacher = ClassTeacher.objects.filter(
		# 	Q(primary_teacher__id=teacherID) | Q(secondary_teacher__id=teacherID))
		# class_list = []
		# for c in class_teacher:
		# 	class_list.append(c.taught_class)
		class_list = Class.objects.filter(
			Q(classteacher__primary_teacher__id=teacherID) | 
			Q(classteacher__secondary_teacher__id=teacherID)) 
	else:

		class_list = Class.objects.filter(
			school = request.user_school, 
			period = request.user_period
		).order_by('course')

	filters, class_list = class_list_helper(request, class_list)

	context_dictionary = { 
		'class_list': class_list, 
		'class_filter': filters }

	if class_id:
		try:
			c = Class.objects.get(pk=class_id)
			if c.school != request.user_school or c.period != request.user_period:
				raise ObjectDoesNotExist
			context_dictionary['class'] = c
			context_dictionary['enrolled'] = c.enrolled_class.filter(registration_status=True).count()
			context_dictionary['waiting'] = c.enrolled_class.filter(registration_status=False).count()
		except ObjectDoesNotExist:
				context_dictionary['error'] = 'There is no class in this school and period with that id.'
	 
	return render_to_response("classes/class_list.html",
		context_dictionary,
		RequestContext(request))

def class_list_helper(request, class_list):
	search_course = request.GET.get('course', None)
	search_section = request.GET.get('section', None)  
	search_dept = request.GET.get('department', None)  
	
	if search_course:
		class_list = class_list.filter(
			course__name__icontains=search_course)

	if search_section:
		class_list = class_list.filter(
			section__icontains=search_section)

	if search_dept:
		class_list = class_list.filter(
			course__department__name__icontains=search_dept)

	filters = ClassFilter(
			{'course': search_course, 'section': search_section, 'department': search_dept})

	return filters, class_list


@login_required
def class_create(request):

	request = process_user_info(request)

	if (request.user_role == 'TEACHER'):
		return render_to_response('404.html',RequestContext(request))

	class_form = ClassForm(prefix='info')
	courses = Course.objects.filter(
		school = request.user_school, 
		period = request.user_period
	)

	class_form.fields['course'].queryset = courses
	teacher_form = ClassTeacherForm(prefix='te')
	teachers = TeacherUser.objects.filter(
		user__period = request.user_period, 
		user__school = request.user_school
	)
	teacher_form.fields['primary_teacher'].queryset = teachers
	teacher_form.fields['secondary_teacher'].queryset = teachers
   
	context_dictionary = {
		'class_form': class_form, 
		'classday_form': ClassScheduleForm(prefix='sch'),
		'classteacher_form': teacher_form
	}

	if request.method == 'POST':
		cf = ClassForm(request.POST, prefix='info')
		cf.fields['course'].queryset = courses
		sf = ClassScheduleForm(request.POST, prefix='sch')
		te = ClassTeacherForm(request.POST, prefix='te')
		te.fields['primary_teacher'].queryset = teachers
		te.fields['secondary_teacher'].queryset = teachers
	
		if cf.is_valid() and sf.is_valid() and te.is_valid():
			# save class
			new = cf.save(commit=False)
			new.school = request.user_school
			new.period = request.user_period
			new.save()

			# save class schedule
			schedule = sf.save(commit=False)
			schedule.sch_class = new
			schedule.save()

			# save class teacher
			#try:
			
			teacher = te.save(commit=False)
			teacher.taught_class = new
			teacher.save()
			#except Exception as e:
				# no teacher in request, don't create ClassTeacher object
			#	pass

			return HttpResponseRedirect(
				reverse('school:classlist', args=(new.id,)))
		else:
			context_dictionary['class_errors'] = cf.errors
			context_dictionary['schedule_errors'] = sf.errors
			context_dictionary['teacher_errors'] = te.errors

			context_dictionary['class_form']=cf
			context_dictionary['classday_form']=sf
			context_dictionary['classteacher_form']=te
                        
	return render_to_response('classes/class_form.html',
		context_dictionary,
		RequestContext(request))

'''
Delete Class
'''
@login_required
def class_delete(request, class_id):

	request = process_user_info(request)

	if (request.user_role == 'TEACHER'):
		return render_to_response('404.html',RequestContext(request))

	sc_class = Class.objects.get(pk=class_id)
	ClassSchedule.objects.filter(sch_class=sc_class).delete()
	ClassRegistration.objects.filter(reg_class=sc_class).delete()
	ClassAttendance.objects.filter(reg_class=sc_class).delete()
	Grading.objects.filter(reg_class=sc_class).delete()
	Assignment.objects.filter(reg_class=sc_class).delete()
	sc_class.delete()
	messages.success(request, "Class has been deleted!")
	return redirect('school:classlist')

# why do we have 2??
# def class_registration(request, class_id=None):
# 	request = process_user_info(request)

# 	if (request.user_role == 'TEACHER'):
# 		return render_to_response('404.html',RequestContext(request))

# 	if request.POST:
# 		return class_registration_helper(request, class_id)

# 	else:
# 		class_list = Class.objects.filter(
# 			school = request.user_school, 
# 			period = request.user_period).order_by('course')
# 		context_dictionary = {'class_list': class_list }

# 		if class_id:
# 			cl = Class.objects.get(pk=class_id)
# 			context_dictionary['class'] = cl 
# 			context_dictionary['student_list'] = Student.objects.all()
# 			context_dictionary['form'] = ClassRegistrationForm()
# 			context_dictionary['remove_form'] = RemoveClassRegistrationForm()
		
# 		return render_to_response("classes/class_registration.html",
# 			context_dictionary,
# 			RequestContext(request))

@login_required
def class_edit(request, class_id):
		request = process_user_info(request)

		if (request.user_role == 'TEACHER'):
			return render_to_response('404.html',RequestContext(request))
                
		class_list = Class.objects.filter(
		school = request.user_school, 
		period = request.user_period).order_by('course')

		filters, class_list = class_list_helper(request, class_list)

		context_dictionary = {'class_list': class_list, 'class_filter': filters}

		try:
				c = Class.objects.get(pk=class_id)
				if c.school != request.user_school or c.period != request.user_period:
					raise ObjectDoesNotExist
			
				context_dictionary['class_id'] = class_id
			
                                        #context_dictionary['shalala'] = 'shalala'

				s = c.schedule #all classes created normally (through the form) should have this...
                         
                                        #context_dictionary['here'] = 'here' #for testing

				t = c.classteacher #class can only have one classteacher
                                       # context_dictionary['ha'] = 'ha'# for testing

				class_form = ClassForm(prefix='info', instance = c)
				courses = Course.objects.filter(
					school = request.user_school, 
					period = request.user_period
				)
				class_form.fields['course'].queryset = courses
				classday_form = ClassScheduleForm(prefix='sch', instance = s)
				classteacher_form = ClassTeacherForm(prefix='te', instance = t)
				teachers = TeacherUser.objects.filter(user__school=request.user_school, user__period=request.user_period)
				classteacher_form.fields['primary_teacher'].queryset = teachers
				classteacher_form.fields['secondary_teacher'].queryset = teachers
	
				if request.method == 'POST':
						class_form = ClassForm(request.POST, prefix='info', instance = c)
						classday_form = ClassScheduleForm(request.POST, prefix='sch', instance = s)
						classteacher_form = ClassTeacherForm(request.POST, prefix='te', instance = t)

						teachers = TeacherUser.objects.filter(user__school=request.user_school, user__period=request.user_period)
						classteacher_form.fields['primary_teacher'].queryset = teachers
						classteacher_form.fields['secondary_teacher'].queryset = teachers
						class_form.fields['course'].queryset = courses
                                
						if class_form.is_valid() and classday_form.is_valid() and classteacher_form.is_valid():
								class_form.save()
								classday_form.save()
								classteacher_form.save()
								context_dictionary['succ']=True
								
				context_dictionary['class_form'] = class_form
				context_dictionary['classday_form'] = classday_form
				context_dictionary['classteacher_form'] = classteacher_form
				
		except ObjectDoesNotExist:
				context_dictionary['error'] = 'There is no class in this school and period with that id.'
						
		return render_to_response("classes/class_edit.html",context_dictionary,RequestContext(request))

@login_required
def class_registration(request, class_id=None):
        
	request = process_user_info(request)

	if (request.user_role == 'TEACHER'): 
		return render_to_response('404.html',RequestContext(request))
        

	if request.POST:
		return class_registration_helper(request, class_id)

	else:
		class_list = Class.objects.filter(
			school = request.user_school, 
			period = request.user_period).order_by('course')
		context_dictionary = {'class_list': class_list }

		if class_id:
			cl = Class.objects.get(pk=class_id)
			context_dictionary['class'] = cl 
			context_dictionary['student_list'] = Student.objects.filter(
				school = request.user_school
			)
			context_dictionary['form'] = ClassRegistrationForm()
			context_dictionary['remove_form'] = RemoveClassRegistrationForm()
			context_dictionary['enrolled'] = cl.enrolled_class.filter(registration_status=True).count()
			context_dictionary['waiting'] = cl.enrolled_class.filter(registration_status=False).count()
		
		return render_to_response("classes/class_registration.html",
			context_dictionary,
			RequestContext(request))

# register student to class
@login_required
def class_registration_helper(request, class_id):

	request = process_user_info(request)
        
	student_id = request.POST['student_id']
	student = Student.objects.get(pk=student_id)

	student_name =  request.POST.get('student_name', None)
	if student_name:
		try:
			student_name = student_name.strip()
			assert(len(student_name.split(' ')) == 2)
			first_name, last_name = student_name.split(' ')
			assert(first_name == student.first_name)
			assert(last_name == student.last_name)

		except AssertionError:
			return HttpResponseBadRequest("Please select a valid student.")

	
	# check if on waiting list
	reg = student.enrolled_student.filter(reg_class__id=class_id, registration_status=False)
	if len(reg) > 0:
		class_reg = reg[0]
		class_reg.registration_status = True
		class_reg.save()
		return HttpResponse("Successfully registered.")

	try:
		reg_class = Class.objects.get(pk=class_id)
		school = request.user_school
		period = request.user_period
		cr = ClassRegistration(
			reg_class=reg_class, student=student, school=school, 
			period=period, registration_status=True)

		cr.save()

		#add none grades for student for all existent assignments in the class
		existent_assignments_list = Assignment.objects.filter(reg_class=reg_class)
		if len(existent_assignments_list)!=0:
			for a in existent_assignments_list:
				verify = Grading.objects.filter(student=student, reg_class=reg_class, assignment=a)
				if len(verify) == 0:
					Grading.objects.create(student =student, reg_class=reg_class, assignment=a, performance=None, grade=None)


		return HttpResponse("Successfully registered.")
	except IntegrityError:
		return HttpResponseBadRequest("This student is already registered.")
	
	except Exception as e:
		return HttpResponseBadRequest(e)

# delete student from class
@login_required
def class_remove_registration(request, class_id):

	request = process_user_info(request)
        
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

@login_required
def class_attendance(request, class_id=None):

	request = process_user_info(request)
        
	if request.user_role == 'TEACHER':
		teacherID = request.user_profile.teachers.first().id
		# class_teacher = ClassTeacher.objects.filter(
		# 	Q(primary_teacher__id=teacherID) | Q(secondary_teacher__id=teacherID))
		# class_list = []
		# for c in class_teacher:
		# 	class_list.append(c.taught_class)
		class_list = Class.objects.filter(
			Q(classteacher__primary_teacher__id=teacherID) | 
			Q(classteacher__secondary_teacher__id=teacherID)) 
	else:

		class_list = Class.objects.filter(
			school = request.user_school, 
			period = request.user_period
		).order_by('course')

	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c

		class_reg_list = ClassRegistration.objects.filter(reg_class__id = class_id).order_by('student__first_name')
		context_dictionary['classregistration'] = class_reg_list

		AttendanceFormSetFactory = modelformset_factory(ClassAttendance,extra=0, can_delete=True)
		date_form = ClassAttendanceDateForm()
		context_dictionary['dateform'] = date_form

		if request.method == "POST":

				if '_date' in request.POST:

					date_form = ClassAttendanceDateForm(request.POST)

					if date_form.is_valid():
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

						query_list = ClassAttendance.objects.filter(date=date_value)
						formset = AttendanceFormSetFactory(queryset=query_list)
						context_dictionary['formset'] = formset
						context_dictionary['querylist'] = query_list

						date_form = ClassAttendanceDateForm(initial={'date': date_value})
						context_dictionary['dateform'] = date_form
					else:
						context_dictionary['date_errors'] = date_form.errors

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

							context_dictionary['success'] = "Attendance was saved successfully."
						
						create_attendance_notifications(request, c)

					else:
						context_dictionary['errors'] = formset.errors

					context_dictionary['date_value'] = date_value

					query_list = ClassAttendance.objects.filter(date=date_value)
					formset = AttendanceFormSetFactory(queryset=query_list)
					context_dictionary['formset'] = formset
					context_dictionary['querylist'] = query_list

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

				query_list = ClassAttendance.objects.filter(date=date_value)
				context_dictionary['querylist'] = query_list
				formset = AttendanceFormSetFactory(queryset=query_list)
		
		context_dictionary['dateform'] = date_form
		context_dictionary['formset'] = formset

	return render_to_response('classes/class_attendance.html', context_dictionary,
		RequestContext(request))

def create_attendance_notifications(request, class_):
	attendance_notification = NotificationType.objects.get(notification_type='Attendance')
	max_absences = attendance_notification.condition

	#  get all absences in the class
	absences = ClassAttendance.objects.filter(
		reg_class=class_, attendance='A'
	).order_by('student', 'date')

	curr_student = None
	last_absence = 0
	first_absence = 0
	absent_streak = 0

	for absence in absences:

		# if not the same student, check streak and reset
		if curr_student is None or curr_student.id != absence.student.id: 		
			absent_streak = 1
			first_absence = absence.date
			last_absence = absence.date.toordinal()
			curr_student = absence.student

		# if consecutive, increase streak and store date
		elif absence.date.toordinal() - last_absence == 1:
			absent_streak += 1
			last_absence = absence.date.toordinal()

		if absent_streak >= max_absences:
			# check if attendance notification already exists for this student
			# creates another notification only if start of absence is different
			notif_list = Notification.objects.filter(
				notification_type=attendance_notification,
				student=curr_student,
				date=first_absence
				)
			if len(notif_list) == 0:
				notification = Notification(
					notification_type=attendance_notification, 
					student=curr_student,
					school=request.user_school,
					period=request.user_period,
					date=first_absence,
					status=False)
				notification.save()

		 	



@login_required
def class_performance(request, class_id=None, assignment_id=None):

	request = process_user_info(request)

	if request.user_role == 'TEACHER':
		teacherID = request.user_profile.teachers.first().id
		# class_teacher = ClassTeacher.objects.filter(
		# 	Q(primary_teacher__id=teacherID) | Q(secondary_teacher__id=teacherID))
		# class_list = []
		# for c in class_teacher:
		# 	class_list.append(c.taught_class)
		class_list = Class.objects.filter(
			Q(classteacher__primary_teacher__id=teacherID) | 
			Q(classteacher__secondary_teacher__id=teacherID)) 
	else:

		class_list = Class.objects.filter(
			school = request.user_school, 
			period = request.user_period
		).order_by('course')

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
							current.performance = None
							current.save()
						else:
							total = a.total_weight
							current.performance = (grade/total) * 100
							current.save()

					create_performance_notifications(request, c)

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

def create_performance_notifications(request, c):
	performance_notification = NotificationType.objects.get(notification_type='Performance')
	min_performance = performance_notification.condition

	# go over each student in the class
	students = [x.student for x in c.enrolled_class.all()]
	for student in students:
		per = find_overall_performance(student.id)

		# check if unread notification already exists
		notif_list = Notification.objects.filter(
			notification_type=performance_notification,
			student=student,
			status=False
		)

		#  might return None if no assignments yet
		if per is not None and per < min_performance and len(notif_list) == 0:
			notif = Notification(
				notification_type = performance_notification,
				student = student,
				school = request.user_school, 
				period = request.user_period,
				status=False)
			notif.save()

# returns a percent
def find_overall_performance(student_id):
	#  find all the classes this student is registered in
	s = Student.objects.get(pk=student_id)
	classes = [x.reg_class for x in s.enrolled_student.all()]
	grand_total = len(classes) * 100
	class_total = sum(filter(None, 
		[find_class_performance(student_id, c.id) for c in classes]))

	if grand_total == 0:
		return None

	return class_total/grand_total * 100

#  returns a percent
def find_class_performance(student_id, class_id):
		
		student = Student.objects.get(pk=student_id)
		c = Class.objects.get(pk=class_id)
		performances = Grading.objects.filter(student=student, reg_class=c)
		total_performance = 0 # in percent, weighted by assignment weight
		total_weight = 0

		# for each performance, multiply by each weight 
		for per in performances:
			if per.performance != None:
				weight = per.assignment.grade_weight
				total_weight = total_weight + weight
				total_performance += per.performance * weight	


		if (total_weight == 0):
			return None

		return total_performance/total_weight


@login_required
def class_assignment(request, class_id=None):

	request = process_user_info(request)
	
	if request.user_role == 'TEACHER':
		teacherID = request.user_profile.teachers.first().id
		# class_teacher = ClassTeacher.objects.filter(
		# 	Q(primary_teacher__id=teacherID) | Q(secondary_teacher__id=teacherID))
		# class_list = []
		# for c in class_teacher:
		# 	class_list.append(c.taught_class)
		class_list = Class.objects.filter(
			Q(classteacher__primary_teacher__id=teacherID) | 
			Q(classteacher__secondary_teacher__id=teacherID)) 
	else:

		class_list = Class.objects.filter(
			school = request.user_school, 
			period = request.user_period
		).order_by('course')

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
				#new.content = request.FILES['content']
				new.save()

				#create grades for assignments				
				class_reg_list = ClassRegistration.objects.filter(reg_class__id = class_id).order_by('student__first_name')

				a = Assignment.objects.get(pk=new.id)
				for cl in class_reg_list:
					verify = Grading.objects.filter(student=cl.student, reg_class=c, assignment=a)
					if len(verify) == 0:
						Grading.objects.create(student =cl.student, reg_class=c, assignment=a, performance=None, grade=None)



				# Redirect to the document list after POST
				return HttpResponseRedirect(
					reverse('school:classassignment', args=(class_id,)))
		else:
			form = ClassAssignmentForm()

		context_dictionary['form'] = form


	return render_to_response('classes/class_assignment.html', context_dictionary,
		RequestContext(request))

@login_required
def assignment_edit(request, class_id=None, assignment_id=None): #there should always be a period_id here
    #!!! probably block off this view entirely for anybody but system admin !!!
	request = process_user_info(request)
	
	if request.user_role == 'TEACHER':
		teacherID = request.user_profile.teachers.first().id
		# class_teacher = ClassTeacher.objects.filter(
		# 	Q(primary_teacher__id=teacherID) | Q(secondary_teacher__id=teacherID))
		# class_list = []
		# for c in class_teacher:
		# 	class_list.append(c.taught_class)
		class_list = Class.objects.filter(
			Q(classteacher__primary_teacher__id=teacherID) | 
			Q(classteacher__secondary_teacher__id=teacherID)) 
	else:

		class_list = Class.objects.filter(
			school = request.user_school, 
			period = request.user_period
		).order_by('course')

	context_dictionary = { 'class_list': class_list }

	if class_id and assignment_id:

		try:

				a = Assignment.objects.get(pk=assignment_id)
				c = Class.objects.get(pk=class_id)

                #make sure that school admins can only access by url the periods in their school
				if request.user_role == 'SCHOOL_ADMIN' and c.school != request.user_school:
					raise ObjectDoesNotExist
                
				context_dictionary['assignment_id']=assignment_id
				context_dictionary['class_id']=class_id
				
				if request.method == 'POST':
					assignment_form = ClassAssignmentForm(request.POST, request.FILES, instance = a)
					if assignment_form.is_valid():
						assignment_form.save()
						context_dictionary['success']=True

						#also update performance
						a = Assignment.objects.get(pk = assignment_id)
						grading_list = Grading.objects.filter(reg_class=c, assignment=a)

						for current in grading_list:
							grade = current.grade

							if grade == None:
								current.performance = None
								current.save()

							else:
								total = a.total_weight
								current.performance = (grade/total) * 100
								current.save()

						#also create new notifications
						create_performance_notifications(request, c)

						return HttpResponseRedirect(reverse('school:classassignment', args=(class_id,)))

				else:
					assignment_form = ClassAssignmentForm(instance = a)
                        
				context_dictionary['assignment_form'] = assignment_form

		except ObjectDoesNotExist:
				context_dictionary['error'] = 'No assignment with this id.'

		return render_to_response("classes/class_assignment_edit.html",
                        context_dictionary,
                        RequestContext(request))


@login_required
def class_reportcard(request, class_id=None, student_id=None):

	request = process_user_info(request)
        
	if request.user_role == 'TEACHER':
		teacherID = request.user_profile.teachers.first().id
		# class_teacher = ClassTeacher.objects.filter(
		# 	Q(primary_teacher__id=teacherID) | Q(secondary_teacher__id=teacherID))
		# class_list = []
		# for c in class_teacher:
		# 	class_list.append(c.taught_class)
		class_list = Class.objects.filter(
			Q(classteacher__primary_teacher__id=teacherID) | 
			Q(classteacher__secondary_teacher__id=teacherID)) 
	else:

		class_list = Class.objects.filter(
			school = request.user_school, 
			period = request.user_period
		).order_by('course')

	context_dictionary = { 'class_list': class_list }

	if class_id:
		c = Class.objects.get(pk=class_id)
		context_dictionary['class'] = c

	if student_id:
		s = Student.objects.get(pk=student_id)
		context_dictionary['student'] = s

		grading_list = Grading.objects.filter(student=s, reg_class=c).order_by('-assignment__date').reverse()
		context_dictionary['gradinglist'] = grading_list


		if len(grading_list) == 0:
			context_dictionary['performancemessage'] = '*No assignments available to grade the student in this class.'
			
		else:
			#cont none for grades
			cont_none = 0
			for g in grading_list:
				if g.grade == None:
					cont_none = cont_none + 1
			
			if cont_none == 0: #has all grades
				context_dictionary['performancemessage'] = ''

			if cont_none > 0: #missing some grades
				context_dictionary['performancemessage'] = '*Performance do not consider missing grades. Insert missing grades for an accurate performance.'

			total = len(grading_list)
			if total == cont_none: #missing all grades
				context_dictionary['performancemessage'] = '*No grades available.'
				

	
		# context_dictionary['overall'] = average
		context_dictionary['overall'] = find_class_performance(student_id, c.id)

	return render_to_response('classes/class_reportcard.html', context_dictionary,
		RequestContext(request))
