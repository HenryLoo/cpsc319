from django.contrib import admin
from school_components.models import Student, Parent, Course, Prerequisite, Department

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Course)
admin.site.register(Prerequisite)
admin.site.register(Department)