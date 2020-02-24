# -*- coding: utf-8 -*-


import requests
from requests.adapters import HTTPAdapter
from fake_useragent import UserAgent


def getHtml(url):
    ua = UserAgent()
    useragent = ua.random
    headers = {
        'User-Agent': useragent
    }
    try:
        response = requests.get(url, headers=headers)
        return response
    except requests.exceptions as e:
        print(e)
