from django.db import models

class Attendance(models.Model):
    studentID = models.IntegerField(blank = True, null = True)
    classID = models.IntegerField(blank = True, null = True)
    status = models.IntegerField(blank = True, null = True)

class Grade(models.Model):
    studentID = models.IntegerField(blank = True, null = True)
    classID = models.IntegerField(blank = True, null = True)
    assignmentID = models.IntegerField(blank = True, null = True)
    grade = models.IntegerField(blank = True, null = True)