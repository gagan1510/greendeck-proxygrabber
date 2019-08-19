import json
import requests
import sys
from greendeck_proxygrabber.src.proxygrabber.proxygrabber import ProxyGrabber
from greendeck_proxygrabber.src.proxygrabber.proxychecker import ProxyChecker
from greendeck_proxygrabber.src.proxygrabber.country_proxy_grabber import ScrapeProxy
import time

proxies = {}

def test_proxy_scraper():
    http, https = ScrapeProxy.proxy_scraper()
    assert (len(http) > 0) and (len(https) > 0)

def test_proxy_grabber():
    global proxies
    proxy = ProxyGrabber(len_proxy_list=1, timeout=2, country_code='ALL')
    proxies = proxy.grab_proxy()
    print(proxies)
    assert len(proxies['http']) == len(proxies['https']) == 1

def test_proxy_checker():
    proxy_list_http = proxies['http']
    proxy_list_https = proxies['https']

    ip_http = []
    ip_https = []
    for proxy in proxy_list_http:
        proxy_dict = {
            'http': 'http://{}'.format(proxy)
        }
        item = requests.get('http://api.ipify.org', proxies = proxy_dict)
        ip_http.append(item.text)
    
    for proxy in proxy_list_https:
        proxy_dict = {
            'https': 'https://{}'.format(proxy)
        }
        item = requests.get('https://api.ipify.org', proxies = proxy_dict)
        ip_https.append(item.text)
    
    assert (len(ip_http)==len(proxy_list_http)) and (len(ip_https)==len(proxy_list_https))
