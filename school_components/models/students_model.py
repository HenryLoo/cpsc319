from django.db import models
from school_components.models.parents_model import Parent

class Student(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	gender = models.CharField(max_length=6,
							choices=(('MALE', 'M'),
									('FEMALE', 'F')))
	birthdate = models.DateField(blank=True)
	home_phone = models.CharField(max_length=20)
	address = models.CharField(max_length=75)
	email = models.EmailField(blank=True)
	allergies = models.CharField(max_length=75, blank=True)
	emergency_contact_name = models.CharField(max_length=75)
	emergency_contact_phone = models.CharField(max_length=20)
	parent = models.ForeignKey('Parent', null=True)
	# school = models.ForeignKey('School')

	class Meta:
		app_label = 'school_components'

