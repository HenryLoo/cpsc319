from django.views import generic
from school_components.models.students_model import Student

class StudentList(generic.ListView):
	model = Student
	template_name = "students/student_list.html"

class StudentDetailView(generic.DetailView):
	model = Student
	template_name = 'student/student_detail.html'
