from django.db import models

class Period(models.Model):
    description = models.CharField(max_length = 50)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    school = models.ForeignKey('School')

    def __unicode__(self):
    	return self.description
    
    class Meta:
        app_label = 'school_components'


