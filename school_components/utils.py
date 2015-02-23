from school_components.models.students_model import Student
from django.forms.models import model_to_dict
from aplus.settings import UPLOAD_PATH
import os

class SchoolUtils:

	@staticmethod
	def parse_csv(file):
		result = []
		for line in file:
			std = map(lambda x: x.strip(), line.split(','))
			s = Student.objects.create_student(*std)
			s.save()
			result.append(model_to_dict(s))
		return result