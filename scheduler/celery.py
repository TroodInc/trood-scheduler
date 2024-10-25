from __future__ import absolute_import
import os
from django.conf import settings
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')
from configurations import importer
importer.install()
from celery import Celery

# set the default Django settings module for the 'celery' program.


app = Celery('scheduler')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
