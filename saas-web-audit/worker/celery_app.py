
# worker/celery_app.py
import os
from celery import Celery

broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
backend_url = broker_url
celery_app = Celery('web_audit', broker=broker_url, backend=backend_url)
celery_app.conf.task_routes = { 'worker.tasks.run_audit_task': {'queue': 'audits'} }
