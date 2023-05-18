import os
from celery import Celery
from datetime import timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_new_products-every_day": {
        "task": "main.tasks.send_new_products",
        "schedule": timedelta(minutes=1)
    }
}