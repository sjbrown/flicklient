from __future__ import absolute_import
from celery import Celery

BROKER_URL = 'django://'
#BROKER_URL = 'redis://localhost'

app = Celery('tasks', broker=BROKER_URL)
app.conf.update(
     CELERY_ACCEPT_CONTENT = ['json'],
     CELERY_TASK_SERIALIZER = 'json',
     CELERY_RESULT_SERIALIZER = 'json',
)

@app.task
def add(x, y):
    return x + y

