import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chemistry_shop.settings")

app = Celery("chemistry_shop")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "cleanup-expired-sessions": {
        "task": "core.tasks.cleanup_expired_sessions",
        "schedule": crontab(hour=1, minute=0),
    },
    "cleanup-jwt-tokens": {
        "task": "core.tasks.cleanup_blacklisted_tokens",
        "schedule": crontab(hour=5, minute=0),
    },
    "health-check": {
        "task": "core.tasks.system_health_check",
        "schedule": crontab(hour=6, minute=0),
    },
}

app.conf.timezone = "UTC"


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
