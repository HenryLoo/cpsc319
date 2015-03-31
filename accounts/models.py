# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

#User table comes complete with import User with:
#the username for the user account;
#the account’s password;
#the user’s email address;
#the user’s first name; and
#the user’s surname.

class UserProfile(models.Model):
    ADMIN_ROLES = ['CODE', 'SYSTEM_ADMIN', 'SCHOOL_ADMIN']
    
    # This line is required. Links UserProfile to a User model instance.
    user = models.ForeignKey(User, blank=True,null=True, related_name='userprofiles')
    phone_regex = RegexValidator(regex=r'^[\d|-]+$', message="Use only digits and dashes, eg. 604-214-0392")
    # The additional attributes we wish to include.
    school = models.ForeignKey('school_components.School',blank=True, null=True)
    period = models.ForeignKey('school_components.Period', blank=True, null=True)
    phone = models.CharField(max_length = 20, validators=[phone_regex], blank=True, null=True,)
    role = models.CharField(max_length = 12, choices =
                            (
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
    user = models.ForeignKey(UserProfile, blank=True,null=True, related_name='teachers')
    teaching_availability = models.ForeignKey(TeachingAvailability, blank=True,null=True)
    comments = models.CharField(max_length = 500, blank=True, null=True)
    #classes has a many-to-many relation with this

    def __unicode__(self):
        return self.user.user.first_name + " " + self.user.user.last_name


