import os
import django
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_dashboard.settings')

app = Celery('music_dashboard', include=['music_dashboard.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'collect-music-spotify-api':{
        'task': 'music_dashboard.tasks.collect',
        'schedule': crontab(minute = 1)
    }
}

django.setup()