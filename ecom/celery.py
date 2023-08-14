from __future__ import absolute_import,unicode_literals
import os
import json
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
#Gets default config module name from enviromental variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'ecom.settings')
app=Celery("ecom")
app.conf.enable_utc=False
app.conf.update(timezone="Asia/Kathmandu")#Timezone needed for scheduling tasks
#Config is necessary to determine how celery works
#Loads config form settings which is config object and contains configuration Attribute
app.config_from_object(settings,namespace="CELERY")

#Time to schedule our api calls task in tasks.py using this configuration
app.conf.beat_schedule={
        
               }

app.autodiscover_tasks()#Celery will automatically detect our tasks
@app.task(bind=True)
def debug_task(self):
    print(f"RESULT:{self.request!r}")