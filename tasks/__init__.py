import os

from celery import Celery, platforms

from tasks import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper_zl.settings')

platforms.C_FORCE_ROOT = True

celery_app = Celery("tasks")
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()




