# -*- coding: utf-8 -*-


# https://www.kuaidaili.com/free/inha/1/
# https://www.xicidaili.com/nn/
# http://www.89ip.cn/index_3.html
# http://www.nimadaili.com/putong/
# http://www.66ip.cn/1.html
# https://www.freeip.top/?page=1
# http://www.ip3366.net/free/


import re
import time
from utils import utilFunction
from lxml import etree


class ProxyMetaclass(type):
    def __new__(cls, name, bases, dicts):
        count = 0
        dicts['__crawlFunc__'] = []
        for k, v in dicts.items():
            if 'proxy_' in k:
                dicts['__crawlFunc__'].append(k)
                count += 1
        dicts['__crawlCount__'] = count
        return super(ProxyMetaclass, cls).__new__(cls, name, bases, dicts)


class Proxy(metaclass=ProxyMetaclass):
    def getproxies(self, callback):
        proxies = []
        print("Current crawl website %s" % callback)
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
        return proxies

    def proxy_xicidaili(self):
        url_list = [
            'https://www.xicidaili.com/nn',
            'https://www.xicidaili.com/nt'
        ]
        for url in url_list:
            time.sleep(10)
            response = utilFunction.getHtml(url)
            content = response.text
            html = etree.HTML(content)
            tds = html.xpath(".//table[@id='ip_list']/tr[position()>1]/td[2]|.//table[@id='ip_list']/tr[position()>1]/td[3]")
            for i in range(0, len(tds), 2):
                proxy = tds[i].text + ':' + tds[i+1].text
                yield proxy

    def proxy_eigthnine(self):
        base = "http://www.89ip.cn/index_"
        url_list = [base + str(page) + '.html' for page in range(1, 5)]
        for url in url_list:
            time.sleep(10)
            response = utilFunction.getHtml(url)
            html = etree.HTML(response.text)
            tds = html.xpath('.//tbody/tr/td[position()<3]')
            for i in range(0, len(tds), 2):
                proxy = tds[i].text.strip() + ':' + tds[i + 1].text.strip()
                yield proxy

    def proxy_sixsix(self):
        base = 'http://www.66ip.cn/'
        url_list = [base + str(page) + '.html' for page in range(1, 5)]
        for url in url_list:
            time.sleep(10)
            html = etree.HTML(utilFunction.getHtml(url).text)
            tds = html.xpath('.//div[@class="containerbox boxindex"]//table/tr[position()>1]/td[position()<3]')
            for i in range(0, len(tds), 2):
                proxy = tds[i].text + ':' + tds[i + 1].text
                yield proxy

    def proxy_freeip(self):
        base = 'https://www.freeip.top/?page='
        url_list = [base + str(page) for page in range(1, 5)]
        for url in url_list:
            time.sleep(10)
            content = utilFunction.getHtml(url).text
            html = etree.HTML(content)
            tds = html.xpath('.//table/tbody/tr/td[position()<3]')
            for i in range(0, len(tds), 2):
                proxy = tds[i].text + ':' + tds[i + 1].text
                yield proxy

    def proxy_kuaidaili(self):
        url_list = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/'
        ]
        for url in url_list:
            for page in range(1, 4):
                ip_url = url + str(page) + '/'
                time.sleep(10)
                response = utilFunction.getHtml(ip_url)
                content = response.text
                pattern = re.compile('<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>')
                ips = pattern.findall(content)
                for address, port in ips:
                    proxy = address + ':' + port
                    yield proxy.replace(' ', '')


if __name__ == '__main__':
    p = Proxy()
    for callback in p.__crawlFunc__:
        p.getproxies(callback)
