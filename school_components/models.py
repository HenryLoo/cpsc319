from django.db import models

class Schools(models.Model):
    
    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, null = True)
    address = models.CharField(max_length = 200)


class Periods(models.Model):
    
    description = models.CharField(max_length = 50)
    school = models.ForeignKey(Schools)