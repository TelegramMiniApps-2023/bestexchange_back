import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_transport_options = {'visibility_timeout': 1800}

app.autodiscover_tasks()