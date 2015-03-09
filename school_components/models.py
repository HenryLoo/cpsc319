from django.db import models

class School(models.Model):
    location = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, null = True)
    address = models.CharField(max_length = 200)
   
   class Meta:
        app_label = 'school_components'

class Period(models.Model):
    description = models.CharField(max_length = 50)
    school = models.ForeignKey(School)

    class Meta:
        app_label = 'school_components'

class Parent(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    home_phone = models.CharField(max_length=20)
    cell_phone = models.CharField(max_length=20)
    email = models.EmailField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
        
        
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
        
    class Meta:
        app_label = 'school_components'