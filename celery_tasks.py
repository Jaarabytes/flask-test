import os
from celery import Celery

def make_celery(app):
    # Create a new Celery object and configure it with Flask's config
    celery = Celery(
        app.import_name,
        broker=os.environ.get('BROKER_URL', 'redis://localhost:6379/0'),
        backend=os.environ.get('RESULT_BACKEND', 'redis://localhost:6379/0')
    )
    celery.conf.update(app.config)
    return celery
