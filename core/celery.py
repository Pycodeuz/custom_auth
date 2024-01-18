from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False

app.conf.update(timezone='Asia/Tashkent')

app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

# CELERY BEAT SETTINGS

# app.conf.beat_schedule = {
#     'send-ad-mail-every-day': {
#         'task': 'users.email.send_email',
#         'schedule': crontab(hour=15, minute=56),
#         'args': ("I am the best.",)
#     }
# }

app.autodiscover_tasks()

# celery -A core worker -l info
