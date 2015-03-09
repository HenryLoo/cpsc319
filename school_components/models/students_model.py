from django.db import models
from datetime import datetime, date
from school_components.models.parents_model import Parent

# used to create students from CSV
# what to do if parent is not in the system already?
# TODO: parent
class StudentManager(models.Manager):
	def create_student(self, first_name, last_name, gender, birthdate, home_phone,
		address, email, allergies, emergency_contact_name, emergency_contact_phone):

		bd = datetime.strptime(birthdate, "%Y-%m-%d").date()
		p = Parent.objects.get(pk=1)


		student = self.create(first_name=first_name, last_name=last_name, gender=gender, 
			birthdate=bd, home_phone=home_phone, address=address, email=email, 
			allergies=allergies, emergency_contact_name=emergency_contact_name, 
			emergency_contact_phone=emergency_contact_phone, parent=p)

		return student

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

	objects = StudentManager()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	class Meta:
		app_label = 'school_components'

class StudentCSVWriter(object):
	def write(self, value):
		return value


