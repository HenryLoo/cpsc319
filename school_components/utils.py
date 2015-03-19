from school_components.models.students_model import Student
from django.forms.models import model_to_dict
from datetime import datetime


class SchoolUtils:

	@staticmethod
	#  used to check csv for errors
	def validate_csv(file):
		student_list = []
		errors = []

		for i, line in enumerate(file):
			# check for number of args
			try:
				std = map(lambda x: x.strip(), line.split(','))
				if len(std) != 15:
					raise ValueError("Incorrect number of arguments on line %d." % i)

				s = Student.objects.create_student(*std)
				student_list.append(s)

			except Exception as e:
				errors.append(str(e))

			if len(errors) > 10:
				return None, errors

		return student_list, errors

	@staticmethod
	def parse_csv(file):
		for line in file:
			std = map(lambda x: x.strip(), line.split(','))
			s = Student.objects.create_student(*std)
			s.save()
			result.append(model_to_dict(s))
		return result
