from sna.db.Mongo import Database as MongoDB
from sna.scraping.twitter.Scraper import Scraper
import sna.task
from sna.helper.encoder import JSONEncoder
from urllib.parse import unquote
import numpy
import json

db = MongoDB()
scraper = Scraper()
worker = sna.task.worker
request_limit = 200
tweet_per_request = 100
limit_per_minute = 15



@worker.task(name='Scraping.twitter', bind=True)
def twitterscrap(self, keyword):

    try:
        keyword = keyword.split(',')

        for key in keyword:
            scraper.searchtweet(key, count=1000)
        return str(','.join(keyword)) + ' Sukses Diproses'
    except Exception as e:
        return str(keyword) + str(e)


@worker.task(name='Scraping.twitter.continue_scrap_forward')
def continue_scrap_future():
    db.initialize('twitter_dump2')
    collection = db.list_collection()
    keyword_request_per_minute = request_limit / limit_per_minute / len(collection) / 2 * tweet_per_request
    for col in collection:
        since_id = list(db.order_tweet_id(col, order=-1))
        scraper.searchtweet(query=col, count=int(keyword_request_per_minute),
                            since_id=int(since_id[0]['tweet_id']))
    return 'Crawl Scheduler Sukses'


@worker.task(name='Scraping.twitter.continue_scrap_backward')
def continue_scrap_pass():
    db.initialize('twitter_dump2')
    collection = db.list_collection()
    keyword_request_per_minute = request_limit / limit_per_minute / len(collection) / 2 * tweet_per_request
    for col in collection:
        max_id = list(db.order_tweet_id(col, order=1))
        scraper.searchtweet(query=col, count=int(keyword_request_per_minute),
                            max_id=int(max_id[0]['tweet_id']))

    return 'Crawl Scheduler Pass Sukses'


@worker.task(name='Scheduler.twitter.redis_cache')
def redis_cache():
    pass