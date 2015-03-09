from django.db import models

class Course(models.Model):
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	department = models.ForeignKey('Department')
	name = models.CharField(max_length=50, unique=True)
	age_requirement = models.IntegerField(default=0)
	description = models.CharField(max_length=250, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		app_label = 'school_components'


class Prerequisite(models.Model):
	course = models.ForeignKey('Course')
	prereq = models.ForeignKey('Course', related_name='prereq')

	def __unicode__(self):
		return self.course.name + ' ' + self.prereq.name

	class Meta:
		app_label = 'school_components'


class Department(models.Model):
	school = models.ForeignKey('School')
	description = models.CharField(max_length=250)

	def __unicode__(self):
		return self.description

	class Meta:
		app_label = 'school_components'


class CourseRegistration(models.Model):
	course = models.ForeignKey('Course')
	student = models.ForeignKey('Student')
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		app_label = 'school_components'

