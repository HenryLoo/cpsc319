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
    title = models.CharField(max_length = 18)
    school = models.ForeignKey('school_components.School')
    period = models.ForeignKey('school_components.Period')
    chart_type = models.CharField(max_length = 12, choices =
                                   (
                                    ('BAR', 'Bar'),
                                    ('PIE', 'Pie'),
                                    ('LINE', 'Line'),
                                    ))

    x_axis = models.CharField(max_length = 20, choices =
                            (
                               ('SCHOOL', 'School'),
                               ('PERIOD', 'Period'),
                               ('COURSE', 'Courses'),
                            ))

    y_axis = models.CharField(max_length = 20, choices =
                            (
                               ('NSTUDENTS', '# of Students'),
                               ('NCLASSES', '# of Classes'),
                               ('NTEACHERS', '# of Teachers'),
                               ('ATTENDANCE', 'Attendance'),
                               ('PERFORMANCE', 'Performance'),
                            ))
                              
    visibility = models.CharField(max_length = 12, choices =
                                  (
                                ('ADM', 'Only Admins'),
                                          ('ALL', 'All'),
                                          ))