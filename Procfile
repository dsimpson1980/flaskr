web: gunicorn run_server:app
init: python db_create.py
worker: celery -A tasks worker -B --loglevel=info