from django.db import models
from datetime import datetime, date
from school_components.models.parents_model import Parent
from school_components.models.school_model import School
from school_components.models.period_model import Period

# used to create students from CSV
# TODO: update with whatever we're doing for school and period
class StudentManager(models.Manager):
	def create_student(self, first_name, last_name, gender, birthdate, home_phone,
		address, email, allergies, emergency_contact_name, emergency_contact_phone, relation,
		parent_first_name, parent_last_name, parent_cell_phone, parent_email, period, school):

		bd = datetime.strptime(birthdate, "%Y-%m-%d").date()

		parent_defaults = {
			'cell_phone': parent_cell_phone,
			'email': parent_email,
			'school': school,
			'period': period
		}

		parent, pcreated = Parent.objects.get_or_create(
			first_name=parent_first_name, 
			last_name=parent_last_name,
			defaults=parent_defaults)

		if not pcreated:
			for attr, value in parent_defaults.iteritems():
				setattr(parent, attr, value)
			parent.save()

		student_defaults = {
			'home_phone': home_phone,
			'birthdate': birthdate,
			'gender' : gender,
			'address': address,
			'email': email,
			'allergies': allergies,
			'emergency_contact_name' : emergency_contact_name,
			'emergency_contact_phone' : emergency_contact_phone,
			'relation' : relation,
			'parent': parent,
			'school': school,
			'period': period
		}

		student, screated = Student.objects.get_or_create(
			first_name=first_name, 
			last_name=last_name,
			defaults=student_defaults)

		if not screated:
			for attr, value in student_defaults.iteritems():
				setattr(student, attr, value)
			student.save()

		return student

class Student(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	gender = models.CharField(max_length=6,
							choices=(('M', 'M'),
									('F', 'F')))
	birthdate = models.DateField(blank=True)
	home_phone = models.CharField(max_length=20)
	address = models.CharField(max_length=75)
	email = models.EmailField(blank=True)
	allergies = models.CharField(max_length=75, blank=True)
	emergency_contact_name = models.CharField(max_length=75)
	emergency_contact_phone = models.CharField(max_length=20)
	relation = models.CharField(max_length=75, blank=True)
	comments = models.CharField(max_length=500, blank=True)
	parent = models.ForeignKey('Parent', blank=True, null=True)
	school = models.ForeignKey('School', blank=True, null=True)
	period = models.ForeignKey('Period', blank=True, null=True)

	objects = StudentManager()

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

	def clean_csv_fields(self, exclude=None):
		if len(self.first_name) > 50:
			raise ValueError("Student first name is over 50 characters.")
		if len(self.last_name) > 50:
			raise ValueError("Student last name is over 50 characters.")
		if self.gender not in ['M', 'F']:
			raise ValueError("Gender must be one of M or F.")
		
		# will raise error on its own if invalid
		try:
			datetime.strptime(self.birthdate, "%Y-%m-%d").date()
		except Exception:
			raise ValueError("Birthdate does not match format YYYY-MM-DD.")	
		if len(self.home_phone) > 20:
			raise ValueError("Phone number is over 20 characters.")	
		if len(self.address) > 75:
			raise ValueError("Address is over 75 characters.")	
		if '@' not in self.email:
			raise ValueError("Email is invalid.")
		if len(self.allergies) > 75:
			raise ValueError("Allergies is over 75 characters.")
		if len(self.emergency_contact_name) > 75:
			raise ValueError("Emergency contact name is over 75 characters.")
		if len(self.emergency_contact_phone) > 75:
			raise ValueError("Emergency contact phone is over 20 characters.")
		if len(self.relation) > 75:
			raise ValueError("Emergency contact relation is over 75 characters.")

		return True

	class Meta:
		app_label = 'school_components'
		unique_together = ('first_name', 'last_name', 'period')

class StudentCSVWriter(object):
	def write(self, value):
		return value
