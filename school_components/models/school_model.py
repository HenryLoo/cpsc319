from django.db import models

class School(models.Model):
    location = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, null = True)
    address = models.CharField(max_length = 200)
        
    class Meta:
        app_label = 'school_components'

