from django.contrib import admin
from school_components.models import *

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Course)
admin.site.register(Prerequisite)
admin.site.register(Department)
admin.site.register(Class)
admin.site.register(ClassRegistration)
admin.site.register(CourseRegistration)
admin.site.register(School)
admin.site.register(Period)

