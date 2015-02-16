"""
WSGI config for aplus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/opt/bitnami/apps/django/django_projects/Aplus')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/mysite/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aplus.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
