"""
Django settings for aplus project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import psycopg2

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__) #settings directory
PROJECT_PATH = SETTINGS_DIR #project root
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates') #templates
STATIC_PATH = os.path.join(PROJECT_PATH, 'static') #static file
UPLOAD_PATH = '/tmp'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q+iaoo#+fy6h7swd$v6bs7neny%1j(aj-u9!oo8r_dhx)w=xjn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    'crispy_forms',
    'south',
    'accounts',
    'aplusmessages',
    'school_components',
    'dashboard',
    'graphos',
    'reports',
    #'sendgrid',

)
AUTHENTICATION_BACKENDS = ( 'accounts.backend.NoHashBackend', )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "aplus.context_processors.school_period",
)

ROOT_URLCONF = 'aplus.urls'

WSGI_APPLICATION = 'aplus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'aplus_db',
        'USER': 'aplus_dbadmin',
        'PASSWORD': 'aplus',
        'HOST': 'localhost',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = '/opt/bitnami/apps/django/django_projects/Aplus/aplus/static/'
STATIC_URL = '/static/'

from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('accounts.views.login_view')

STATICFILES_DIRS = (
    #can also be the path in string
    STATIC_PATH,
)

MEDIA_ROOT = '/opt/bitnami/apps/django/django_projects/Aplus/aplus/media/'
MEDIA_URL = '/media/'

# Templates
TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SENDGRID_EMAIL_BACKEND = "sendgrid.backends.SendGridEmailBackend"
EMAIL_BACKEND = SENDGRID_EMAIL_BACKEND
SENDGRID_EMAIL_HOST = "smtp.sendgrid.net"
SENDGRID_EMAIL_PORT = 587
SENDGRID_EMAIL_USERNAME = "sashaseifollahi"
SENDGRID_EMAIL_PASSWORD = "cpsc31911"

# Sample CSV file
SAMPLE_CSV_PATH = "/opt/bitnami/apps/django/django_projects/Aplus/school_components/static/SAMPLE.CSV"
