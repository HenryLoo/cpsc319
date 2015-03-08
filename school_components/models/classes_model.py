from django.db import models
from datetime import time, datetime

class Class(models.Model):
	course = models.ForeignKey('Course')
	# school = models.ForeignKey('School')
	# period = models.ForeignKey('Period')
	section = models.CharField(max_length=50, blank=True)
	description = models.CharField(max_length=250, blank=True)
	start_time = models.TimeField(null=True, blank=True)
	duration = models.DecimalField(max_digits=5, decimal_places=2, default=1)
	room = models.CharField(max_length=50, blank=True)

	def __unicode__(self):
		return self.course.name + ' ' + self.section # + self.period

	class Meta:
		app_label = 'school_components'

# no teachers yet?
# class ClassTeacher(models.Model):
# 	teacher = models.ForeignKey('Teacher')
# 	taught_class = models.ForeignKey('Class')
# 	period = models.ForeignKey('Period')
# 	school = models.ForeignKey('School')

# 	class Meta:
# 		app_label = 'school_components'


class ClassRegistration(models.Model):
	reg_class = models.ForeignKey('Class', related_name='enrolled_class')
	student = models.ForeignKey('Student', related_name='enrolled_student')
	# school = models.ForeignKey('School')
	# period = models.ForeignKey('Period')

	class Meta:
		app_label = 'school_components'





