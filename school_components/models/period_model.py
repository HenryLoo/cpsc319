from django.db import models

class Period(models.Model):
    description = models.CharField(max_length = 50)
    school = models.ForeignKey('School')
    
    class Meta:
        app_label = 'school_components'


