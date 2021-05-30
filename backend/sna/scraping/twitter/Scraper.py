from sna.db.Mongo import Database
from sna.sentiment.SentimentClassifier import SentimentClassifier
import os
import config
import advertools as adv
import pandas as pd


class Scraper(Database):
    classifier = SentimentClassifier()
    auth_params = {
        'app_key': os.getenv('CONSUMER_KEY'),
        'app_secret': os.getenv('CONSUMER_SECRET'),
        'oauth_token': os.getenv('ACCESS_TOKEN'),
        'oauth_token_secret': os.getenv('ACCESS_SECRET'),
    }

    def __init__(self):
        self.dict_label = {0: 'netral', 1: 'positif', 2: 'negatif'}
        try:
            adv.twitter.set_auth_params(**Scraper.auth_params)
        except Exception as e:
            print(e)

    def searchtweet(self, query, geocode=None, lang='id', locale=None, result_type='recent',
                    count=10000, until=None, since_id=None, max_id=None,
                    include_entities=None, tweet_mode='extended'):
        try:
            result = adv.twitter.search(q=query, geocode=geocode, lang=lang, locale=locale, result_type=result_type,
                                        count=count, until=until, since_id=since_id,
                                        max_id=max_id, include_entities=include_entities, tweet_mode=tweet_mode)

            # membuat column sentiment
            result['sentiment'] = Scraper.classifier.predict(list(result['tweet_full_text']))
            result['sentiment'].replace(self.dict_label, inplace=True)

            conn = Database()
            conn.initialize('twitter_dump2')
            conn.create_index_unique(query, 'tweet_id', 'tweet_id')
            conn.insert_many(query, result.T.to_dict().values())
            return 'Data Sudah Di Crawling'

        except Exception as e:
            print(e)
            try:
                # apakah ini di coba lagi
                result['sentiment'] = Scraper.classifier.predict(list(result['tweet_full_text']))
                result['sentiment'].replace(self.dict_label, inplace=True)

                conn = Database()
                conn.initialize('twitter_dump2')
                # conn.make_collection(query, 'twitter_dump')
                conn.create_index_unique(query, 'tweet_id', 'tweet_id')
                conn.insert_many(query, result.T.to_dict().values())

                return 'Sukses'
            except Exception as e:
                return 'Error'

    def user_timeline(self, tweet_id, trim_user=None, tweet_mode='extended'):
        pass

    def tweet_lookup(self):
        pass
