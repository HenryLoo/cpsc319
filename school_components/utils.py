from school_components.models import Student, Parent
from django.forms.models import model_to_dict
from datetime import datetime


class SchoolUtils:

	@staticmethod
	#  used to check csv for errors
	def validate_csv(file):
		errors = []

		for i, line in enumerate(file):
			# check for number of args
			try:
				std = map(lambda x: x.strip(), line.split(','))
				if len(std) != 15:
					# +1 because not line numbers don't start at 0
					raise ValueError("Incorrect number of arguments.")

				student_fields = std[:-4]
				parent_fields = std[-4:]

				Student('', *student_fields).clean_csv_fields()
				Parent('', *parent_fields).clean_csv_fields()

			except Exception as e:
				errors.append("Line %d: %s" % (i+1, str(e)))

			if len(errors) > 10:
				return None, errors

		return errors

	@staticmethod
	def parse_csv(file, period, school):
		result = []
		for line in file:
			std = map(lambda x: x.strip(), line.split(','))
			s = Student.objects.create_student(*std, period=period, school=school)
			result.append(s)
		return result
