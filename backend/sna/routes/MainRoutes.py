from flask_cors import cross_origin
from flask import jsonify, request, escape, Response
from flask import current_app as app
from os import environ, path
from datetime import timezone, datetime
from sna.db.Mongo import Database as MongoDB
from sna.helper.encoder import JSONEncoder
import numpy
import json

db = MongoDB()
twitter_dump = 'twitter_dump2'
db.initialize(twitter_dump)

@cross_origin()
@app.route('/main/keyword')
def list_keyword():
    data = db.list_collection()
    return Response(json.dumps({'result': data}, cls=JSONEncoder), mimetype='application/json')

@cross_origin()
@app.route('/main/drop/<string:query>')
def drop_keyword(query):
    try:
        db.drop_collection(query)
        return f'{query} deleted'
    except:
        return 'Error'

@cross_origin()
@app.route('/test/helloworld', methods=['GET'])
def Helloworld():
    keyword = request.args.get('keyword')
    db.initialize('test')
    data = db.find(keyword, None)
    return json.dumps(list(data), cls=JSONEncoder)


@cross_origin()
@app.route('/test/gettweet/<string:query>', methods=['GET'])
def getTweet(query):
    db.initialize('twitter_dump')
    data = db.project(query, field={"tweet_created_at": 1, "tweet_full_text": 1, "user_screen_name": 1,
                                    "sentiment": 1})
    return json.dumps(list(data), cls=JSONEncoder)


