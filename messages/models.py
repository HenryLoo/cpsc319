from django.core.urlresolvers import reverse
from django.db import models

class SentMessage(models.Model):
    sender = models.CharField(max_length = 100) #email
    recipient = models.CharField(max_length = 12, choices =
                            (
                             ('ALL', 'All'),
                             ('ADMINS', 'All Admins'),
                             ('TEACHERS', 'All Teachers'),
                             ('STUDENTS', 'All Students'),
                             ('CLASS', 'All in class X')
                             ))
    subject = models.CharField(max_length = 50)
    content = models.CharField(max_length = 1000)

#previous:

class Email(models.Model):
	#email = models.CharField(max_length=200)

	def get_absolute_url(self):
		return reverse()

