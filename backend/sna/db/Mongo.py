import pymongo as pm
from collections import Counter
from sna.preprocessor.Extractor import Extractor

class Database:
    URI = 'mongodb://127.0.0.1:27017'
    DATABASE = None

    @staticmethod
    def initialize(db):
        client = pm.MongoClient(Database.URI, connect=False)
        Database.DATABASE = client[db]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def insert_many(collection, data):
        Database.DATABASE[collection].insert_many(data, ordered=False)

    @staticmethod
    def update_many(collection, data):
        Database.DATABASE[collection].update(data, data, upsert=True)

    @staticmethod
    def create_index_compound(collection, index_field, index_name):
        Database.DATABASE[collection].create_index([(index_field, pm.TEXT)], name=index_name)

    @staticmethod
    def create_index_unique(collection, index_field, index_name):
        Database.DATABASE[collection].create_index(index_field, name=index_name, unique=True)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def project(collection, field={}):
        return Database.DATABASE[collection].aggregate([{'$project': field}])

    @staticmethod
    def aggregate(collection, field=[]):
        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def list_collection():
        return Database.DATABASE.list_collection_names()

    @staticmethod
    def count_data(collection):
        return Database.DATABASE[collection].aggregate([{'$count': 'count'}])

    @staticmethod
    def make_collection(collection):
        try:
            if collection in Database.list_collection():
                pass
            else:
                Database.DATABASE.create_collection(collection)
                return collection + 'Sukses dibuat'
        except Exception as e:
            return str(e)

    @staticmethod
    def drop_collection(collection):
        try:
            return Database.DATABASE[collection].drop()
        except:
            return "Doesn't Exist"

    @staticmethod
    def order_tweet_id(collection, order=1):
        field = [
            {
                '$sort': {
                    'tweet_id': order
                }
            }, {
                '$limit': 1
            }, {
                '$project': {
                    'tweet_id': 1,
                    'tweet_created_at': 1
                }
            }
        ]
        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def list_collection():
        return Database.DATABASE.list_collection_names()


    # <<< FOR SUMMARY

    @staticmethod
    def count_retweet(collection):
        field = [
            {
                '$group': {
                    '_id': None,
                    'count_retweet': {
                        '$sum': '$tweet_retweet_count'
                    }
                }
            }
        ]
        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def count_likes(collection):
        field = [
            {
                '$group': {
                    '_id': None,
                    'total_favorite': {
                        '$sum': '$tweet_favorite_count'
                    }
                }
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def count_mentions(collection):
        field = [
            {
                '$project': {
                    'count_mentions': {
                        '$size': '$tweet_entities.user_mentions'
                    }
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_mentions': {
                        '$sum': '$count_mentions'
                    }
                }
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def count_reaction(collection):
        likes = list(Database.count_likes(collection))
        retweet = list(Database.count_retweet(collection))
        total = likes[0]['total_favorite'] + retweet[0]['count_retweet']
        return total


    @staticmethod
    def count_sentiment(collection):
        negatif = None
        positif = None
        netral = None

        field = [
            {
                '$group': {
                    '_id': '$sentiment',
                    'total_sentiment': {
                        '$sum': 1
                    }
                }
            }
        ]


        data = list(Database.DATABASE[collection].aggregate(field))

        for sentiment in data:
            if sentiment['_id'] == "negatif":
                negatif = sentiment['total_sentiment']
            if sentiment['_id'] == "positif":
                positif = sentiment['total_sentiment']
            if sentiment['_id'] == "netral":
                netral = sentiment['total_sentiment']

        result = {'total_negatif': negatif, 'total_positif': positif, 'total_netral': netral}

        return result

    ## FOR SUMMARY >>>


    # tweet satuan
    @staticmethod
    def daytoday(collection, display=20, page=1):
        skip = display * (page - 1)
        field = [
            {
                '$project': {
                    'tweet_created_at': 1,
                    'user_screen_name': 1,
                    'tweet_full_text': 1,
                    'sentiment': 1
                }
            }, {
                '$sort': {
                    'tweet_id': -1
                }
            }, {
                '$skip': skip
            }, {
                '$limit': display
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

    ## <<< FOR CHART BY DAY
    @staticmethod
    def tweetcountbyday(collection):
        field = [
            {
                '$project': {
                    'sentiment': 1,
                    'tweet_date': {
                        '$dateToString': {
                            'format': '%d-%m-%Y',
                            'date': '$tweet_created_at'
                        }
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'tweet_date': '$tweet_date'
                    },
                    'total': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    '_id.tweet_date': 1
                }
            }, {
                '$project': {
                    '_id': 0,
                    'total': 1,
                    'date': '$_id.tweet_date'
                }
            }
        ]
        return Database.DATABASE[collection].aggregate(field)


    @staticmethod
    def count_daily_retweet(collection):
        field = [
            {
                '$project': {
                    'tweet_date': {
                        '$dateToString': {
                            'format': '%d-%m-%Y',
                            'date': '$tweet_created_at'
                        }
                    },
                    'tweet_retweet_count': 1
                }
            }, {
                '$group': {
                    '_id': {
                        'tweet_date': '$tweet_date'
                    },
                    'daily_retweet': {
                        '$sum': '$tweet_retweet_count'
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'daily_retweet': 1,
                    'date': '$_id.tweet_date'
                }
            }, {
                '$sort': {
                    'date': 1
                }
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def count_daily_likes(collection):
        field = [
            {
                '$project': {
                    'tweet_date': {
                        '$dateToString': {
                            'format': '%d-%m-%Y',
                            'date': '$tweet_created_at'
                        }
                    },
                    'tweet_favorite_count': 1
                }
            }, {
                '$group': {
                    '_id': {
                        'tweet_date': '$tweet_date'
                    },
                    'daily_likes': {
                        '$sum': '$tweet_favorite_count'
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'daily_likes': 1,
                    'date': '$_id.tweet_date'
                }
            }, {
                '$sort': {
                    'date': 1
                }
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def count_daily_mentions(collection):
        field = [
            {
                '$project': {
                    'tweet_date': {
                        '$dateToString': {
                            'format': '%d-%m-%Y',
                            'date': '$tweet_created_at'
                        }
                    },
                    'tweet_entities': 1
                }
            }, {
                '$group': {
                    '_id': {
                        'tweet_date': '$tweet_date'
                    },
                    'daily_mentions': {
                        '$sum': {
                            '$size': '$tweet_entities.user_mentions'
                        }
                    }
                }
            }, {
                '$project': {
                    '_id': 0,
                    'tweet_date': '$_id.tweet_date',
                    'daily_mentions': 1
                }
            }, {
                '$sort': {
                    'tweet_date': 1
                }
            }
        ]

        return Database.DATABASE[collection].aggregate(field)
    ## FOR CHART BY DAY


    ## <<< FOR CHART SENTIMENT

    @staticmethod
    def count_daily_sentiment(collection):
        field = [
            {
                '$project': {
                    'sentiment': 1,
                    'tweet_date': {
                        '$dateToString': {
                            'format': '%d-%m-%Y',
                            'date': '$tweet_created_at'
                        }
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'tweet_date': '$tweet_date',
                        'sentiment': '$sentiment'
                    },
                    'total': {
                        '$sum': 1
                    }
                }
            }, {
                '$sort': {
                    '_id': 1
                }
            }, {
                '$project': {
                    '_id': 0,
                    'tweet_date': '$_id.tweet_date',
                    'sentiment': '$_id.sentiment',
                    'total_sentiment': '$total'
                }
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

     ## FOR CHART SENTIMENT >>>

     ## FOR CHART SENTIMENT >>>


    @staticmethod
    def count_profile(collection):
        field = [
            {
                '$group': {
                    '_id': '$user_screen_name',
                    'profile': {
                        '$sum': 1
                    }
                }
            },
            {
                '$count': 'total_profile'
            }
        ]
        return Database.DATABASE[collection].aggregate(field)




    @staticmethod
    def topprofile(collection, display=50):
        field = [
            {
                '$project': {
                    'tweet_date': {
                        '$dateToString': {
                            'format': '%d-%m-%Y',
                            'date': '$tweet_created_at'
                        }
                    },
                    '_id': 0,
                    'user_screen_name': 1,
                    'tweet_favorite_count': 1,
                    'tweet_retweet_count': 1,
                    'reaction_count': {
                        '$add': [
                            '$tweet_favorite_count', '$tweet_retweet_count'
                        ]
                    }
                }
            }, {
                '$group': {
                    '_id': {
                        'user_screen_name': '$user_screen_name'
                    },
                    'total_retweet': {
                        '$sum': '$tweet_retweet_count'
                    },
                    'total_likes': {
                        '$sum': '$tweet_favorite_count'
                    }
                }
            }, {
                '$project': {
                    'user_screen_name': '$_id.user_screen_name',
                    'total_likes': 1,
                    'total_retweet': 1,
                    '_id': 0
                }
            }, {
                '$sort': {
                    'total_likes': -1
                }
            }, {
                '$limit': display
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def toptweet(collection, display=50):
        field = [
            {
                '$project': {
                    'tweet_date': {
                        '$dateToString': {
                            'format': '%d-%m-%Y',
                            'date': '$tweet_created_at'
                        }
                    },
                    '_id': 0,
                    'tweet_full_text': 1,
                    'user_screen_name': 1,
                    'likes_count': '$tweet_favorite_count',
                    'retweet_count': '$tweet_retweet_count',
                    'reaction_count': {
                        '$add': [
                            '$tweet_favorite_count', '$tweet_retweet_count'
                        ]
                    }
                }
            }, {
                '$sort': {
                    'likes_count': -1
                }
            }, {
                '$limit': display
            }
        ]

        return Database.DATABASE[collection].aggregate(field)

    @staticmethod
    def tophashtag(collection, display=50):
        field = [
            {
                '$project': {
                    '_id': 0,
                    'hashtags': '$tweet_entities.hashtags.text'
                }
            }
        ]
        hashtags_list = []

        data = Database.DATABASE[collection].aggregate(field)
        try:
            for x in data:
                if x['hashtags'] != []:
                    for l in x['hashtags']:
                        hashtags_list.append(l)

            count_hashtag = Counter(hashtags_list)
            result = [{'hashtags': key, 'total': value} for key, value in sorted(count_hashtag.items(), key=lambda item: -item[1])]
            return result[0:display]
        except Exception as e:
            return str(e)

    @staticmethod
    def topsite(collection):
        field = [
            {
                '$project': {
                    'tweet_urls': '$tweet_entities.urls'
                }
            }
        ]

        data = Database.DATABASE[collection].aggregate(field)
        url_list = Extractor.create_url_list(data, list_url_column='tweet_urls')
        result = Extractor.parallel_url_extractor(url_list)
        result = Counter(result)
        result = [{'site': key, 'total': value} for key, value in sorted(result.items(), key=lambda item: -item[1])]
        return result

    @staticmethod
    def wordcloud(collection):
        field = [
            {
                '$project': {
                    'tweet_full_text': 1,
                    '_id': 0
                }
            }
        ]

        return Database.DATABASE[collection].aggregate(field)
