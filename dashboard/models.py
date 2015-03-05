from django.db import models
from datetime import datetime

class NotificationType(models.Model):
    type = models.CharField(max_length = 12)
    condition = models.IntegerField(blank = False, null = False)
    content = models.CharField(max_length = 100)

class Notification(models.Model):
    type = models.ForeignKey(NotificationType)
    #change for user foreign key
    user = models.CharField(max_length = 12)
    date = models.DateTimeField(default=datetime.now())
    status = models.BooleanField()

class Chart(models.Model):
    title = models.CharField(max_length = 12)
    type = models.CharField(max_length = 12, choices =
                                   (
                                    ('BARS', 'bars chart'),
                                    ('PIE', 'pie chart'),
                                    ('LINE', 'line chart'),
                                    ))
                                    
    x_axis = models.CharField(max_length = 20, choices =
                                  (
                                   ('NSTUDENTS', 'Number of Students'),
                                   ('NCLASSES', 'Number of Classes'),
                                   ('NTEACHERS', 'Number of Teachers'),
                                   ('ATTENDANCE', 'Attendance'),
                                   ('PERFORMANCE', 'Performance'),
                                   ))

    y_axis = models.CharField(max_length = 20, choices =
                            (
                               ('DATE', 'Date'),
                               ('STUDENTS', 'Students'),
                               ('CLASS', 'Classes'),
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
