from django.db import models

class Parent(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	home_phone = models.CharField(max_length=20)
	cell_phone = models.CharField(max_length=20)
	email = models.EmailField()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		app_label = 'school_components'


class Payment(models.Model):
	receipt_no = models.CharField(max_length=50)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	parent = models.ForeignKey('Parent', related_name='payment', null=True)
	# period = models.ForeignKey('Period')

	def __unicode__(self):
		return self.receipt_no

	class Meta:
		app_label = 'school_components'