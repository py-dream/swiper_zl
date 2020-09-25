from celery import Celery
from tasks import config
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper_zl.settings')


celery_app = Celery('tasks')
celery_app.config_from_object(config)

celery_app.autodiscover_tasks()