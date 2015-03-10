from django.db import models
 
import re
import uuid
 
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms
from django.contrib.auth import get_user_model


class TeachingAvailability(models.Model):
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)

    comments = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.teacher_info.user_info.first_name + " " + self.teacher_info.user_info.last_name + "availability"
    


#=============================================================================================

class UserManager(BaseUserManager):
 
  def _create_user(self, email, password, phone, address, school_branch, role, is_staff=False, is_superuser=False, **extra_fields):
    now = timezone.now()
    if not email:
      raise ValueError(_('The given email must be set'))
    email = self.normalize_email(email)
    
    user = self.model(email=email, phone=phone, address=address, school_branch=school_branch, role=role,
             is_staff=is_staff, is_active=True, #hmm let users be active to begin with
             is_superuser=is_superuser, last_login=now,
             date_joined=now, **extra_fields)
    user.set_password(password)
    user.save(using='aplus_db')#using=self._db) #hmm hopefully this is postgre
    return user
 
  #def create_user(self, email, password=None, **extra_fields):
   # return self._create_user(email, password, False, False,
    #             **extra_fields)
 
  def create_superuser(self, email, password, phone, address, school_branch, role,**extra_fields):
    user=self._create_user(email, password, phone, address, school_branch, role, True, True,
                 **extra_fields)
    user.is_active=True
    user.save(using='aplus_db')
    return user


#####================================================================================

 
class User(AbstractBaseUser, PermissionsMixin):
#  username = models.CharField(_('username'), max_length=30, unique=True,
#    help_text=_('Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
#    validators=[
#      validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))
#    ])

  objects = UserManager()
  email = models.EmailField(_('email address'), max_length=255, unique=True)
  first_name = models.CharField(_('first name'), max_length=30)
  last_name = models.CharField(_('last name'), max_length=30)
  phone = models.CharField(_('phone number'), max_length=50, unique=True, help_text=_('7 or 10 digit number, with extensions allowed; delimiters are spaces, dashes, or periods'),
                           validators=[
      validators.RegexValidator(re.compile('^\d+$'),#('''^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|
                                           #([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|
                                           #[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$'''),
                                _('Enter a valid phone number.'), _('invalid'))
    ])
  address = models.CharField(_('address'), max_length=50)
  
  school_branch = models.CharField(_('school branch'), max_length=255)
  role = models.CharField(_('role'), max_length=3, choices=( ('SYS', 'System Admin'),
                                                             ('SCH', 'School Admin'),
                                                             ('TEA', 'Teacher')))
  
  is_staff = models.BooleanField(_('staff status'), default=False,
    help_text=_('Designates whether the user can log into this admin site.'))
  is_active = models.BooleanField(_('active'), default=False,
    help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
 
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address', 'school_branch', 'role']
 
  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
 
  def get_full_name(self):
    full_name = '%s %s' % (self.first_name, self.last_name)
    return full_name.strip()
 
  def get_short_name(self):
    return self.first_name
 
  def email_user(self, subject, message, from_email=None):
    send_mail(subject, message, from_email, [self.email])


#=============================================================================================

class TeacherInfo(models.Model):
    user_info = models.OneToOneField(User, related_name="teacher_info")
    skill_level = models.IntegerField(blank = True, null = True)
    teaching_availability = models.OneToOneField(TeachingAvailability, related_name="teacher_info")
    #classes has a many-to-many relation with this

    def __unicode__(self):
        return self.user_info.first_name + " " + self.user_info.last_name
