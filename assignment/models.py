from django.db import models


# Create your models here.

class Assignment(models.Model):
    assignment_title = models.CharField(max_length=255)
    assignment_date = models.DateTimeField('date created')
    assignment_content = models.CharField(max_length=1000)
