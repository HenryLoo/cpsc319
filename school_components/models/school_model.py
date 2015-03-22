from django.db import models

class School(models.Model):
    title = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, null = True)
    address = models.CharField(max_length = 200)
    comments = models.CharField(max_length = 500)

    def __unicode__(self):
    	return self.title
        
    class Meta:
        app_label = 'school_components'

