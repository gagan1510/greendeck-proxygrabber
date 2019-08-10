import json
import sys
from greendeck_proxygrabber.src.proxygrabber.proxygrabber import ProxyGrabberClass
from greendeck_proxygrabber.src.proxygrabber.proxychecker import ProxyChecker
from greendeck_proxygrabber.src.proxygrabber.country_proxy_grabber import proxy_scraper

proxies = {}

def test_proxy_scraper():
    http, https = proxy_scraper()
    assert (len(http) == 200) and (len(https) == 200)

def test_proxy_grabber():
    global proxies
    proxy = ProxyGrabberClass(len_proxy_list= 1)
    proxies = proxy.grab_proxy()
    assert len(proxies['http']) == len(proxies['https']) == 1

def test_proxy_checker():
    proxy_list = proxies['http']
    checked_http = ProxyChecker.proxy_checker_http(proxy_list = proxy_list, timeout = 2)
    proxy_list = proxies['https']
    checked_https = ProxyChecker.proxy_checker_https(proxy_list = proxy_list, timeout = 2)
    assert (len(checked_http)==len(proxy_list)) and (len(checked_https)==len(proxy_list))