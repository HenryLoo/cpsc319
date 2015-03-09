from django.db import models

class Period(models.Model):
    description = models.CharField(max_length = 50)
    start_date = models.TimeField(null=True, blank=True)
    end_date = models.TimeField(null=True, blank=True)
    school = models.ForeignKey('School')
    
    class Meta:
        app_label = 'school_components'


