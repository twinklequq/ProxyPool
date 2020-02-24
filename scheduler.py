# -*- coding: utf-8 -*-


import asyncio
import aiohttp
import time
try:
    from aiohttp.errors import ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError
from config.settings import *
from ProxyGetter import Proxy
from error import ResourceDepletionError
from asyncio import TimeoutError
from utils.redis_opt import RedisClient
from multiprocessing import Process


class ProxyCheck:
    def __init__(self):
        self._initial_proxies = None
        self._test_url = TEST_URL

    def get_initial_proxies(self, proxies):
        self._initial_proxies = proxies
        self._conn = RedisClient()

    async def test_single_proxy(self, proxy):
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    current_proxy = "http://" + proxy
                    proxy_list = self._conn.get(self._conn.count())
                    async with session.get(self._test_url, proxy=current_proxy, timeout=10) as response:
                        if response.status == 200 and proxy not in proxy_list:
                            self._conn.put(proxy)
                            print("Valid proxy:", proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('Invalid proxy', proxy)
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as s:
            print(s)
            pass

    def test_all_proxies(self):
        loop = asyncio.get_event_loop()
        tasks = [self.test_single_proxy(proxy) for proxy in self._initial_proxies]
        result = loop.run_until_complete(asyncio.wait(tasks))
        print(result)


class PoolThresh:
    def __init__(self, threshold):
        self.threshold = threshold
        self.conn = RedisClient()
        self.check = ProxyCheck()
        self.proxies = Proxy()

    def is_over_threshold(self):
        proxy_count = self.conn.count()
        if proxy_count >= self.threshold:
            return True
        else:
            return False

    def add_into_pool(self):
        print("Add proxy into proxypool....")
        proxy_count = 0
        proxysites = self.proxies.__crawlFunc__
        while not self.is_over_threshold():
            for callback in proxysites:
                proxies = self.proxies.getproxies(callback)
                proxy_count = len(proxies)
                print('%s crawled %d ip, under checking' % (callback, proxy_count))
                self.check.get_initial_proxies(proxies)
                self.check.test_all_proxies()
                if self.is_over_threshold():
                    print('proxypool is full')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError


class Schedule:
    @staticmethod
    def check_proxy(cycle=WAIT_TIME):
        conn = RedisClient()
        check = ProxyCheck()
        while True:
            count = int(0.5 * conn.count())
            if count == 0:
                print('there is no data in pool, please wait...')
                time.sleep(cycle)
            proxies = conn.get(count)
            check.get_initial_proxies(proxies)
            check.test_all_proxies()
            time.sleep(cycle)

    @staticmethod
    def add_proxy(limit=POOL_LIMIT, threshold=POOL_THRESHOLD, cycle=WAIT_TIME):
        conn = RedisClient()
        adder = PoolThresh(threshold)
        while True:
            if conn.count() < limit:
                adder.add_into_pool()
            time.sleep(cycle)

    def run(self):
        valid = Process(target=Schedule.check_proxy)
        add = Process(target=Schedule.add_proxy)
        valid.start()
        add.start()