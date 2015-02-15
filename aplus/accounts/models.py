from django.db import models

class Teachers(models.Model):
    #register questions for survey
    
    email = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, null = True)
    skill_level = models.IntegerField(blank = True, null = True)
    description = models.TextField(max_length = 500)
    status = models.CharField(max_length = 10)


class Users(models.Model):
    #register questions for survey
    
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 500)
    role = models.CharField(max_length = 20, null = True)
    