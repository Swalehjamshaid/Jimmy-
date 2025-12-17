
# worker/tasks.py
from .celery_app import celery_app
from backend.app.workers.tasks import run_audit_task as backend_run

@celery_app.task(name='worker.tasks.run_audit_task')
def run_audit_task(run_id: str, domain: str, max_pages: int, timeout: int, organization_id: str):
    return backend_run(run_id, domain, max_pages, timeout, organization_id)
