import tweepy
from sna.db import Mongo
from sna.sentiment.SentimentClassifier import SentimentClassifier
from os import environ, path
import os
import config


class TweetScraping(Mongo.Database):
    authentication = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    authentication.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
    api = None
    classifier = SentimentClassifier()

    @staticmethod
    def initialize_api(wait_limit=True, rate_limit_notify=True):
        TweetScraping.api = tweepy.API(TweetScraping.authentication, wait_on_rate_limit=wait_limit,
                                       wait_on_rate_limit_notify=rate_limit_notify)

    def search(self, query, result_type='recent', count=100):
        data = tweepy.Cursor(TweetScraping.api.search, q=query, count=count, result_type=result_type,
                             tweet_mode='extended').items(count)
        try:
            for tweet in data:
                if tweet is not []:
                    conn = Mongo.Database()
                    conn.initialize('test')
                    conn.insert(query, tweet._json)
        except Exception as e:
            print(e)

    def search_result(self, query, result_type='recent', count=100):
        data = tweepy.Cursor(TweetScraping.api.search, q=query, count=count, result_type=result_type,
                             tweet_mode='extended').items(count)
        dict_label = {0: 'netral', 1: 'positif', 2: 'negatif'}
        result = []
        try:
            for tweet in data:
                if tweet is not []:
                    tweet._json['sentiment'] = dict_label[TweetScraping.classifier.predict(tweet._json['full_text'])]
                    conn = Mongo.Database()
                    conn.initialize('test')
                    conn.insert(query, tweet._json)
        except Exception as e:
            print(e)



