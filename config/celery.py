import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Sozlamalarni settings.py dan CELERY prefiksi bilan o'qiymiz
app.config_from_object('django.conf:settings', namespace='CELERY')

# Redis brokerini to'g'ridan-to'g'ri shu yerda ham belgilab ketish xavfsizroq
app.conf.broker_url = 'redis://127.0.0.1:6379/0'

app.autodiscover_tasks()