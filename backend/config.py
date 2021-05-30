from os import environ, path
from dotenv import load_dotenv

base_dir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base_dir, '.env'))

class Config:
    """ Flask Configuration from .env files """

    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_APP = 'wsgi.py'
    FLASK_DEBUG = 1
    CORS_HEADER = 'Content-Type'

    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECO = True
    SQLALCHEMY_TRACK_MODIFICATION = False
    CELERY_BROKER_URL = 'mongodb://127.0.0.1:27017'
    MONGODB_BACKEND_SETTINGS = {
        'database': 'system_log',
        'taskmeta_collection': 'task_log'
    }
