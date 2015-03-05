from django.core.urlresolvers import reverse
from django.db import models

class Email(models.Model):
	#email = models.CharField(max_length=200)

	def get_absolute_url(self):
		return reverse()