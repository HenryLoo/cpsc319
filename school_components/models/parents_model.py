from django.db import models

class Parent(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	home_phone = models.CharField(max_length=20)
	cell_phone = models.CharField(max_length=20)
	email = models.EmailField()
	amount_paid = models.DecimalField(max_digits=10, decimal_places=2)


	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		app_label = 'school_components'


