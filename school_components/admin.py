from django.contrib import admin
from school_components.models import Student, Parent, Course, Prerequisite, Department, Class, ClassRegistration, CourseRegistration

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Course)
admin.site.register(Prerequisite)
admin.site.register(Department)
admin.site.register(Class)
admin.site.register(ClassRegistration)
admin.site.register(CourseRegistration)

