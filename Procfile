web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
worker: celery -A app.workers.celery_app.celery_app worker --loglevel=INFO -Q audits
beat: celery -A app.workers.celery_app.celery_app beat --loglevel=INFO
