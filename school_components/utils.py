from school_components.models import Student, Parent
from django.forms.models import model_to_dict
from datetime import datetime
from accounts.models import *
from school_components.models.courses_model import *


class SchoolUtils:
	
	@staticmethod
	def duplicate_teachers(school, old_period, new_period):
                old_teachers = TeacherUser.objects.filter(user__school=school, user__period=old_period)
                for ot in old_teachers:
                    user = ot.user.user
                    op = ot.user
                    np = UserProfile(user=user, school=school, period=new_period, phone=op.phone, role='TEACHER')
                    np.save()
                    oa = ot.teaching_availability
                    na = TeachingAvailability(monday=oa.monday, monday_times=oa.monday_times,
                                              tuesday=oa.tuesday, tuesday_times=oa.tuesday_times,
                                              wednesday=oa.wednesday, wednesday_times=oa.wednesday_times,
                                              thursday=oa.thursday, thursday_times=oa.thursday_times,
                                              friday=oa.friday, friday_times=oa.friday_times)
                    na.save()
                    nt = TeacherUser(user=np, teaching_availability=na, comments=ot.comments)
                    nt.save()
                        
	@staticmethod
	def duplicate_courses(courses, new_period): #courses contains the current period's courses
                for oc in courses:
                        nc = Course(school=oc.school, period=new_period, department=oc.department,
                                    name=oc.name, age_requirement=oc.age_requirement,
                                    description=oc.description)
                        nc.save()
                
                
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
