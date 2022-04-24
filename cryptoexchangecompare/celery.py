import os
from celery import Celery
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'cryptoexchangecompare.settings.development')

app = Celery('cryptoexchangecompare')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.CELERYBEAT_SCHEDULE = {
#     'get_prices': {
#         'task': 'home.tasks.get_prices',
#         'schedule': 5,
#         'args': ()
#     },
#     'get_orderbooks': {
#         'task': 'exchange.tasks.get_orderbooks',
#         'schedule': 5,
#         'args': ()
#     }
# }
