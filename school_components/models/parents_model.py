from django.db import models
from datetime import datetime

class Parent(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	cell_phone = models.CharField(max_length=20)
	email = models.EmailField()
	school = models.ForeignKey('School')
	period = models.ForeignKey('Period')
	comments = models.CharField(max_length=500, blank=True)

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def clean_csv_fields(self, exclude=None):
		if len(self.first_name) > 50:
			raise ValueError("Parent first name is over 50 characters.")
		if len(self.last_name) > 50:
			raise ValueError("Parent last name is over 50 characters.")
		if len(self.cell_phone) > 20:
			raise ValueError("Parent phone number is over 20 characters.")	
		if '@' not in self.email:
			raise ValueError("Parent email is invalid.")
		return True

	class Meta:
		app_label = 'school_components'
		unique_together = ('first_name', 'last_name', 'period')


class Payment(models.Model):
	receipt_no = models.CharField(max_length=50, blank=False, null=False)
	amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	date = models.DateField(null=True, blank=True, default=datetime.now())
	parent = models.ForeignKey('Parent', related_name='payment')

	def __unicode__(self):
		return self.receipt_no

	class Meta:
		app_label = 'school_components'
		ordering = ['date']
