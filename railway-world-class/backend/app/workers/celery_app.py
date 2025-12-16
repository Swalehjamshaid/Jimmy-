
from celery import Celery
import os
celery_app = Celery("audits", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))
celery_app.conf.task_routes = {"app.workers.tasks.*": {"queue": "audits"}}
celery_app.conf.result_expires = 3600
celery_app.conf.beat_schedule = {
    'weekly-audits': {'task': 'app.workers.tasks.schedule_weekly_audits', 'schedule': 7 * 24 * 3600.0},
}
