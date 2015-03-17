from django.db import models
from datetime import datetime

class NotificationType(models.Model):
    notification_type = models.CharField(max_length = 12)
    condition = models.IntegerField(blank = False, null = False)
    content = models.CharField(max_length = 100)

class Notification(models.Model):
    notification_type = models.ForeignKey(NotificationType)
    #change for student foreign key
    student = models.ForeignKey('school_components.Student')
    school = models.ForeignKey('school_components.School')
    period = models.ForeignKey('school_components.Period')
    date = models.DateTimeField(default=datetime.now())
    status = models.BooleanField()

class Chart(models.Model):
    title = models.CharField(max_length = 12)
    school = models.ForeignKey('school_components.School')
    period = models.ForeignKey('school_components.Period')
    chart_type = models.CharField(max_length = 12, choices =
                                   (
                                    ('BAR', 'bar chart'),
                                    ('PIE', 'pie chart'),
                                    ('LINE', 'line chart'),
                                    ))

    x_axis = models.CharField(max_length = 20, choices =
                            (
                               ('DATE', 'Date'),
                               ('STUDENTS', 'Students'),
                               ('CLASS', 'Classes'),
                            ))

    y_axis = models.CharField(max_length = 20, choices =
                            (
                               ('NSTUDENTS', 'Number of Students'),
                               ('NCLASSES', 'Number of Classes'),
                               ('NTEACHERS', 'Number of Teachers'),
                               ('ATTENDANCE', 'Attendance'),
                               ('PERFORMANCE', 'Performance'),
                            ))
                              
    visibility = models.CharField(max_length = 12, choices =
                                  (
                                ('ADM', 'Only Administrators'),
                                          ('ALL', 'Administrators and Teachers'),
                                          ))


#TEST tables that contain data to generate charts

class Attendance(models.Model):
    studentID = models.IntegerField(blank = True, null = True)
    classID = models.IntegerField(blank = True, null = True)
    status = models.IntegerField(blank = True, null = True)

class Grade(models.Model):
    studentID = models.IntegerField(blank = True, null = True)
    classID = models.IntegerField(blank = True, null = True)
    assignmentID = models.IntegerField(blank = True, null = True)
    grade = models.IntegerField(blank = True, null = True)

