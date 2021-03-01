import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sbservice.settings')

app = Celery('sbservice')
app.conf.broker_url = 'redis://localhost:6379'
app.conf.result_backend = 'redis://localhost:6379'

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))