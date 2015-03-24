from django.db import models
from datetime import time, datetime

class Class(models.Model):
	course = models.ForeignKey('Course')
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	section = models.CharField(max_length=50, blank=True)
	description = models.CharField(max_length=250, blank=True)
	class_size = models.IntegerField(null=True, blank=True)
	waiting_list_size = models.IntegerField(null=True, blank=True)
	room = models.CharField(max_length=50, blank=True)

	# used in displaying class history
	def __unicode__(self):
		return self.course.name + ' ' + self.section 

	class Meta:
		app_label = 'school_components'
		unique_together = ('course', 'section', 'period')

class ClassSchedule(models.Model):
	# needs to be null to allow class to be created first from form
	sch_class = models.OneToOneField('Class', related_name='schedule', null=True)
	monday = models.BooleanField(default=False)
	tuesday = models.BooleanField(default=False)
	wednesday = models.BooleanField(default=False)
	thursday = models.BooleanField(default=False)
	friday = models.BooleanField(default=False)
	saturday = models.BooleanField(default=False)
	sunday = models.BooleanField(default=False)
	start_time = models.TimeField(
		default=datetime(2008, 1, 31, 9, 00, 00), blank=True)
	end_time = models.TimeField(
		default=datetime(2008, 1, 31, 10, 00, 00), blank=True)

	def __unicode__(self):
		result = []
		if self.monday:
			result.append("MON")
		if self.tuesday:
			result.append("TUES")
		if self.wednesday:
			result.append("WED")
		if self.thursday:
			result.append("THURS")
		if self.friday:
			result.append("FRI")
		if self.saturday:
			result.append("SAT")
		if self.sunday:
			result.append("SUN")

		start = time.strftime(self.start_time, '%H:%M %p')
		end = time.strftime(self.end_time, '%H:%M %p')
		return '%s %s-%s' % ('/'.join(result), start, end)


	class Meta:
		app_label = 'school_components'


class ClassTeacher(models.Model):
	# needs to be null to allow class to be created 
	teacher = models.ForeignKey('accounts.TeacherUser', related_name='teacher')
	taught_class = models.ForeignKey('Class', related_name='taught_class', null=True)

	class Meta:
		app_label = 'school_components'
		unique_together = ('teacher', 'taught_class')


class ClassRegistration(models.Model):
	reg_class = models.ForeignKey('Class', related_name='enrolled_class')
	student = models.ForeignKey('Student', related_name='enrolled_student')
	registration_status = models.BooleanField()
	date = models.DateTimeField(auto_now_add=True, blank=True)
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')

	# used in sorting on registration page
	def class_period(self):
		return self.reg_class.period

	class Meta:
		app_label = 'school_components'
		unique_together = ('reg_class', 'student')


#change name after
class ClassAttendance(models.Model):
	reg_class = models.ForeignKey('Class')
	student = models.ForeignKey('Student')
	attendance = models.CharField(max_length=5, blank=True)
	date = models.TimeField(null=True, blank=True)
	comments = models.CharField(max_length=500)

	class Meta:
		app_label = 'school_components'
		unique_together = ('reg_class', 'student', 'date')

class Assignment(models.Model):
	reg_class = models.ForeignKey('Class')
	title = models.CharField(max_length=100, blank=True)
	date = models.DateField(null=True, blank=True)
	#saves pdf at file assignments inside media at aplus file
	content = models.FileField(upload_to='aplus/media/assignments', blank = True, null = True)
	grade_weight = models.IntegerField(blank = True, null = True)
	total_weight = models.IntegerField(blank = True, null = True)
	comments = models.CharField(max_length=500)

	class Meta:
		app_label = 'school_components'

class Grading(models.Model):
	g_id = models.IntegerField(blank=True, null=True)
	reg_class = models.ForeignKey('Class')
	student = models.ForeignKey('Student')
	grade = models.IntegerField(blank=True, null=True)
	assignment = models.ForeignKey('Assignment')
	comments = models.CharField(max_length=500)

	class Meta:
		app_label = 'school_components'
