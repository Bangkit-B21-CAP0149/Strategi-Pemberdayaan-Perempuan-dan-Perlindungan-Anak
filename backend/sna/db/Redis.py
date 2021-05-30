import redis
import json

class Red:
    def __init__(self):
        self.rds = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    def set(self, cache_key, api):
        api = json.dumps(api)
        self.rds.set(cache_key, api)

    def get(self, cache_key):
        cache_data = self.rds.get(cache_key)
        if cache_data:
            cache_data = cache_data.decode('utf-8')
            cache_data = json.loads(cache_data)
            return cache_data
        else:
            return None
