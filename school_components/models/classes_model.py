from django.db import models
from datetime import time, datetime

class Class(models.Model):
	course = models.ForeignKey('Course')
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	section = models.CharField(max_length=50, blank=True)
	description = models.CharField(max_length=250, blank=True)
	class_size = models.IntegerField(blank = True, null = True)
	waiting_list_size = models.IntegerField(blank = True, null = True)
	room = models.CharField(max_length=50, blank=True)

	def __unicode__(self):
		return self.course.name + ' ' + self.section # + self.period

	class Meta:
		app_label = 'school_components'

class ClassSchedule(models.Model):
	sch_class = models.ForeignKey('Class')
	weekday = models.CharField(max_length = 12, choices =
                            (
                             ('Mon', 'Monday'),
                             ('Tue', 'Tuesday'),
                             ('Wed', 'Wednesday'),
                             ('Thu', 'Thursday'),
                             ('Fri', 'Friday')
                             ))
	start_time = models.TimeField(null=True, blank=True)
	end_time = models.TimeField(null=True, blank=True)

	class Meta:
		app_label = 'school_components'


class ClassTeacher(models.Model):
	teacher = models.ForeignKey('accounts.TeacherUser')
	taught_class = models.ForeignKey('Class')
	period = models.ForeignKey('Period')
	school = models.ForeignKey('School')

	class Meta:
		app_label = 'school_components'


class ClassRegistration(models.Model):
	reg_class = models.ForeignKey('Class', related_name='enrolled_class')
	student = models.ForeignKey('Student', related_name='enrolled_student')
	registration_status = models.BooleanField()

	class Meta:
		app_label = 'school_components'


#change name after
class ClassAttendance(models.Model):
	reg_class = models.ForeignKey('Class')
	student = models.ForeignKey('Student')
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	attendance = models.CharField(max_length=5, blank=True)
	date = models.TimeField(null=True, blank=True)
	comments = models.CharField(max_length=500)

	class Meta:
		app_label = 'school_components'

class Assignment(models.Model):
	reg_class = models.ForeignKey('Class')
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	title = models.CharField(max_length=100, blank=True)
	date = models.TimeField(null=True, blank=True)

	#change - how to store pdf
	content = models.CharField(max_length=10, blank=True)
	grade_weight = models.IntegerField(blank = True, null = True)
	total_weight = models.IntegerField(blank = True, null = True)

	class Meta:
		app_label = 'school_components'

class Grading(models.Model):
	reg_class = models.ForeignKey('Class')
	student = models.ForeignKey('Student')
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	grade = models.CharField(max_length=5, blank=True)
	assignment = models.CharField(max_length=100, blank=True)
	date = models.TimeField(null=True, blank=True)
	comments = models.CharField(max_length=500)
	grade_weight = models.IntegerField(blank = True, null = True)
	total_weight = models.IntegerField(blank = True, null = True)

	class Meta:
		app_label = 'school_components'
