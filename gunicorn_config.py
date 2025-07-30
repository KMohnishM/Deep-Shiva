import os

# Gunicorn configuration for Render deployment
workers = int(os.environ.get('GUNICORN_WORKERS', 2))
threads = int(os.environ.get('GUNICORN_THREADS', 4))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 120))
bind = "0.0.0.0:" + os.environ.get('PORT', '5000')
worker_class = 'gevent'
loglevel = 'info'
accesslog = '-'
errorlog = '-'