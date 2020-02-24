# -*- coding: utf-8 -*-


import redis
from config.settings import HOST, PORT, PASSWORD
from error import PoolEmptyError


class RedisClient:
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        proxies = self._db.lrange('self_proxy', 0, count-1)
        self._db.ltrim('self_proxy', count, -1)
        return proxies

    def put(self, proxy):
        self._db.rpush("self_proxy", proxy)

    def pop(self):
        try:
            return self._db.rpop("self_proxy").decode('utf-8')
        except:
            raise PoolEmptyError

    def count(self):
        return self._db.llen("self_proxy")

    def fflush(self):
        self._db.flushall()
        self._db.flushall()
