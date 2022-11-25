from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management.settings')
app = Celery('hospital_management')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'Send_mail_to_Client': {
        'task': 'doctor_app.tasks.send_mail_task',
        'schedule': crontab(hour=12, minute=11, day_of_month='25')
        # 'schedule': 30.0
        # 'args': (2,) you can pass arguments also if rquired
    }
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
