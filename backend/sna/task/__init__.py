from config import Config
from celery import Celery
from celery.schedules import crontab

worker = Celery(__name__)
worker.conf.broker_url = Config.CELERY_BROKER_URL
worker.conf.result_backend = Config.CELERY_BROKER_URL
worker.conf.mongodb_backend_settings = Config.MONGODB_BACKEND_SETTINGS
worker.conf.beat_schedule = {
    '30-minutes-scraper-future': {
        'task': 'Scraping.twitter.continue_scrap_forward',
        'schedule': crontab(minute='*'),
    },
    '30-minutes-scraper-pass': {
        'task': 'Scraping.twitter.continue_scrap_backward',
        'schedule': crontab(minute='*'),
    },
}
