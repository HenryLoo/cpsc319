from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    user_info = models.CharField(max_length = 100) #email
    password = models.CharField(max_length = 12)
    role = models.CharField(max_length = 12, choices =
                            (
                             ('CODE', 'Code Administrator'),
                             ('SYSTEM_ADMIN', 'System Administrator'),
                             ('SCHOOL_ADMIN', 'School Administrator'),
                             ('TEACHER', 'Teacher')
                             ))
                             
    def __unicode__(self):
        return self.user_info.first_name + self.user_info.last_name + "role"

class SchoolAdminUser(models.Model):
    user_info = models.ForeignKey(User)
    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, verbose_name="Phone number")
    #change for foreign key to school
    school = models.CharField(max_length = 100, help_text = "Enter the location of the Gobind Sarvar branch. Make sure to be completely consistent with these.")
    
    def __unicode__(self):
        return self.user_info.first_name + self.user_info.last_name

class TeachingAvailability(models.Model):
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()

    def __unicode__(self):
        return self.teacher_info.user_info.first_name + " " + self.teacher_info.user_info.last_name + "availability"
    
class TeacherUser(models.Model):
    user_info = models.ForeignKey(User)
    name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 15, verbose_name="Phone number")
    #models.RegexField(regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    #change for foreign key to school
    school = models.CharField(max_length = 100, help_text = "Enter the location of the Gobind Sarvar branch. Make sure to be completely consistent with these.")
    skill_level = models.IntegerField(blank = True, null = True)
    teaching_availability = models.ForeignKey(TeachingAvailability)
    #classes has a many-to-many relation with this

    def __unicode__(self):
        return self.user_info.first_name + " " + self.user_info.last_name + "role"

