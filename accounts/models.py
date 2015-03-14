# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User

#User table comes complete with import User with:
#the username for the user account;
#the account’s password;
#the user’s email address;
#the user’s first name; and
#the user’s surname.

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    school = models.ForeignKey('school_components.School')
    period = models.ForeignKey('school_components.Period')
    phone = models.CharField(max_length = 15, blank=True, null=True)
    role = models.CharField(max_length = 12, choices =
                            (
                             ('CODE', 'Code Administrator'),
                             ('SYSTEM_ADMIN', 'System Administrator'),
                             ('SCHOOL_ADMIN', 'School Administrator'),
                             ('TEACHER', 'Teacher')
                             ))

    def __unicode__(self):
        return self.user.username

class TeachingAvailability(models.Model):
    monday = models.NullBooleanField()
    monday_times = models.CharField(max_length = 500, blank=True, null=True)
    tuesday = models.NullBooleanField()
    tuesday_times = models.CharField(max_length = 500, blank=True, null=True)
    wednesday = models.NullBooleanField()
    wednesday_times = models.CharField(max_length = 500, blank=True, null=True)
    thursday = models.NullBooleanField()
    thursday_times = models.CharField(max_length = 500, blank=True, null=True)
    friday = models.NullBooleanField()
    friday_times = models.CharField(max_length = 500, blank=True, null=True)

    
class TeacherUser(models.Model):
    user = models.ForeignKey(UserProfile)
    first_name = models.CharField(max_length = 15, blank=True, null=True)
    last_name = models.CharField(max_length = 15, blank=True, null=True)
    teaching_availability = models.ForeignKey(TeachingAvailability, null=True)
    comments = models.CharField(max_length = 500)
    #classes has a many-to-many relation with this

    def __unicode__(self):
        return self.user.user.first_name + " " + self.user.user.last_name + "role"

