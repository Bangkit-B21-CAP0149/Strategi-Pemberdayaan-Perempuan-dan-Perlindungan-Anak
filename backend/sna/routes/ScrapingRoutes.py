from flask_cors import cross_origin
from flask import jsonify, request, escape
from flask import current_app as app
from os import environ, path

from sna.task.TwitterScrapingWorker import *
from sna.db.Mongo import Database

from datetime import timezone, datetime
from urllib.parse import unquote


db = MongoDB()
twitter_dump = 'twitter_dump2'

@app.route('/twitter/scrap', methods=['GET'])
def twitterscrapworker():
    keyword = unquote(request.args.get('keyword'))
    collection = keyword.split(',')
    for col in (collection):
        db.initialize(twitter_dump)
        db.make_collection(col)
    # nnti keywordnya dalam bentuk apa? = list of string
    twitterscrap.delay(keyword)

    return keyword
