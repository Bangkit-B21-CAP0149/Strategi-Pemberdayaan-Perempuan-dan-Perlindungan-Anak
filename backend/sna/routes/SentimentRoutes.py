from flask_cors import cross_origin
from flask import jsonify, request, escape, Response
from flask import current_app as app
from os import environ, path
from datetime import timezone, datetime
from sna.db.Mongo import Database as MongoDB
from sna.helper.encoder import JSONEncoder
from urllib.parse import unquote
from sna.db.Redis import Red
from sna.preprocessor.Wordcloud import Wordcloud
import numpy
import json

db = MongoDB()
redis_cache = Red()
twitter_dump = 'twitter_dump2'

@cross_origin()
@app.route('/sentiment/summary/<string:query>', methods=['GET'])
def summary(query):
    db.initialize(twitter_dump)
    try:
        cache_key = query + ' summary data cache'
        cache_data = redis_cache.get(cache_key)
        if cache_data:
            return {'result': cache_data}

        query = unquote(query)
        tweet_count = list(db.count_data(query))
        mentions = list(db.count_mentions(query))
        likes = list(db.count_likes(query))
        retweet = list(db.count_retweet(query))
        reaction = db.count_reaction(query)
        profile = list(db.count_profile(query))
        sentiment = db.count_sentiment(query)

        data = {
            'total_tweet': tweet_count[0]['count'],
            'total_mentions': mentions[0]['total_mentions'],
            'total_likes': likes[0]['total_favorite'],
            'total_retweet': retweet[0]['count_retweet'],
            'total_reaction': reaction,
            'total_profile': profile[0]['total_profile'],
            'total_positif': sentiment['total_positif'],
            'total_negatif': sentiment['total_negatif'],
            'total_netral': sentiment['total_netral']
        }

        redis_cache.set(query + ' summary data cache', data)
        return jsonify({'result': data})
    except Exception as e:
        print(e)
        return str(e)


@cross_origin()
@app.route('/sentiment/daytoday/<string:query>', methods=['GET'])
def daytoday(query):
    db.initialize(twitter_dump)
    try:
        query = unquote(query)
        page = unquote(request.args.get('page', default='1', type=str))
        display = unquote(request.args.get('display', default='20', type=str))
        data = db.daytoday(query, int(display), int(page))
        return Response(json.dumps({'result': list(data)}, cls=JSONEncoder), mimetype='application/json')

    except Exception:

        return []

@cross_origin()
@app.route('/sentiment/tweetbyday/<string:query>', methods=['GET'])
def tweetbyday(query):
    db.initialize(twitter_dump)
    cache_key = query + ' daily tweet count data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.tweetcountbyday(query))

    redis_cache.set(query + ' daily tweet count data cache', data)
    return Response(json.dumps({'result': data}, cls=JSONEncoder), mimetype='application/json')

@cross_origin()
@app.route('/sentiment/countdailysentiment/<string:query>')
def countdailysentiment(query):
    db.initialize(twitter_dump)
    cache_key = query + ' daily sentiment data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.count_daily_sentiment(query))

    redis_cache.set(query + ' daily sentiment data cache', data)
    return Response(json.dumps({'result': data}, cls=JSONEncoder), mimetype='application/json')


@cross_origin()
@app.route('/sentiment/countdailylikes/<string:query>')
def countdailylikes(query):
    db.initialize(twitter_dump)
    cache_key = query + ' daily likes data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.count_daily_likes(query))

    redis_cache.set(query + ' daily likes data cache', data)
    return Response(json.dumps({'result': data}, cls=JSONEncoder), mimetype='application/json')


@cross_origin()
@app.route('/sentiment/countdailyretweet/<string:query>')
def countdailyretweet(query):
    db.initialize(twitter_dump)
    cache_key = query + ' daily likes data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.count_daily_retweet(query))

    redis_cache.set(query + ' daily likes data cache', data)
    return Response(json.dumps({'result': data}, cls=JSONEncoder), mimetype='application/json')


@cross_origin()
@app.route('/sentiment/countdailymentions/<string:query>')
def countdailymentions(query):
    db.initialize(twitter_dump)
    cache_key = query + ' daily mentions data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.count_daily_mentions(query))

    redis_cache.set(query + ' daily mentions data cache', data)
    return Response(json.dumps({'result': data}, cls=JSONEncoder), mimetype='application/json')

@cross_origin()
@app.route('/sentiment/toptweet/<string:query>', methods=['GET'])
def toptweet(query):
    db.initialize(twitter_dump)
    cache_key = query + ' top tweet data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.toptweet(query))

    redis_cache.set(query + ' top tweet data cache', data)
    return Response(json.dumps({'result': data}, cls=JSONEncoder), mimetype='application/json')

@cross_origin()
@app.route('/sentiment/topprofile/<string:query>', methods=['GET'])
def topprofile(query):
    db.initialize(twitter_dump)
    cache_key = query + ' top profile data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.topprofile(query))

    redis_cache.set(query + ' top profile data cache', data)
    return Response(json.dumps({'result': list(data)}, cls=JSONEncoder), mimetype='application/json')

@cross_origin()
@app.route('/sentiment/tophashtag/<string:query>', methods=['GET'])
def tophashtag(query):
    db.initialize(twitter_dump)
    cache_key = query + ' top hashtag data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = db.tophashtag(query)

    redis_cache.set(query + ' top hashtag data cache', data)
    return Response(json.dumps({'result': list(data)}, cls=JSONEncoder), mimetype='application/json')

@cross_origin()
@app.route('/sentiment/sitestatistic/<string:query>', methods=['GET'])
def sitestatistic(query):
    db.initialize(twitter_dump)
    cache_key = query + ' site statistic data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = db.topsite(query)

    redis_cache.set(query + ' site statistic data cache', data)
    return Response(json.dumps({'count_site': len(data), 'result': data}, cls=JSONEncoder), mimetype='application/json')

@cross_origin()
@app.route('/sentiment/wordcloud/<string:query>')
def wordcloud(query):
    db.initialize(twitter_dump)
    cache_key = query + ' wordcloud data cache'
    cache_data = redis_cache.get(cache_key)
    if cache_data:
        return {'result': cache_data}

    query = unquote(query)
    data = list(db.wordcloud(query))
    result = Wordcloud.output_data(data, 'tweet_full_text')
    redis_cache.set(query + ' wordcloud data cache', result)
    return Response(json.dumps({'result': result}, cls=JSONEncoder), mimetype='application/json')
