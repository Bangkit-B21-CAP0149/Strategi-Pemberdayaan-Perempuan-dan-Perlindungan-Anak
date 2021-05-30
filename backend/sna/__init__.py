# Copyright (c) 2021 Tim Data Kecilin
"""
This repo provide sentiment analysis with network analysis using networkx
"""

from flask import Flask
from flask_cors import CORS
from celery import Celery
from config import Config

application = Flask(__name__, instance_relative_config=False)

def create_app():

    app = application
    app.config.from_object('config.Config')
    app.run(host='0.0.0.0')
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    with app.app_context():
        from .routes import MainRoutes
        from .routes import SentimentRoutes
        from .routes import ScrapingRoutes
        from .routes import VRRoutes
        return app


worker = Celery(__name__)
worker.conf.broker_url = Config.CELERY_BROKER_URL
worker.conf.result_backend = Config.CELERY_BROKER_URL
worker.conf.mongodb_backend_settings = Config.MONGODB_BACKEND_SETTINGS
