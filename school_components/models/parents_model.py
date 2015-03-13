from django.db import models

class Parent(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	cell_phone = models.CharField(max_length=20)
	email = models.EmailField()
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	comments = models.CharField(max_length=500)

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		app_label = 'school_components'


class Payment(models.Model):
	receipt_no = models.CharField(max_length=50)
	amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	date = models.DateField(null=True, blank=True)
	parent = models.ForeignKey('Parent', related_name='payment')
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')

	def __unicode__(self):
		return self.receipt_no

	class Meta:
		app_label = 'school_components'