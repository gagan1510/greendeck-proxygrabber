# !/usr/bin/env python
import time
from queue import Queue
from threading import Thread
import lxml
import requests
from lxml import html
from lxml.html import fromstring
from .proxychecker import ProxyChecker
from .country_proxy_grabber import proxy_scraper
import sys

class ProxyGrabber():
    proxy_list=[]

    def __init__(
        self, 
        len_proxy_list = 10, 
        country_code = 'ALL', 
        timeout = 2, 
        to_json = True,
        update_time = 120
        ):

        self.len_proxy_list = len_proxy_list
        self.country_code = country_code
        self.timeout = timeout
        self.to_json = to_json
        self.update_time = update_time


    def __grab_proxy_list(self):

        final_proxies = {
            'http': set(),
            'https': set(),
            'region' : 'ALL'
        }
        total_http_checked = 0
        total_https_checked = 0
        remaining_len_http = self.len_proxy_list
        remaining_len_https = self.len_proxy_list
        while (remaining_len_http > 0) or (remaining_len_https > 0):
            scraped_proxies_http, scraped_proxies_https = proxy_scraper(country_code = self.country_code,
                                                                        scraped_http_length = total_http_checked,
                                                                        scraped_https_length = total_https_checked,
                                                                        required_http_len = remaining_len_http, 
                                                                        required_https_len = remaining_len_https,
                                                                        batch=200
                                                                        )
            count_http = 0
            count_https = 0

            total_http_checked += len(scraped_proxies_http)
            total_https_checked += len(scraped_proxies_https)
            
            if len(scraped_proxies_http) or len(scraped_proxies_https):
                checked_http = ProxyChecker.proxy_checker_http(scraped_proxies_http, self.timeout)
                checked_https = ProxyChecker.proxy_checker_https(scraped_proxies_https, self.timeout)
            else:
                print('Maximum possible IPs fetched!')
                break

            if len(final_proxies['http']) < self.len_proxy_list:
                for proxy in checked_http:
                    if proxy and (len(final_proxies['http']) < self.len_proxy_list):
                        count_http += 1
                        final_proxies['http'].add(proxy)

            if len(final_proxies['https']) < self.len_proxy_list:
                for proxy in checked_https:
                    if proxy and (len(final_proxies['https']) < self.len_proxy_list):
                        count_https += 1
                        final_proxies['https'].add(proxy)

            remaining_len_http = remaining_len_http - count_http
            remaining_len_https = remaining_len_https - count_https
            
            remaining_len_http = max(remaining_len_http, 0)
            remaining_len_https = max(remaining_len_https, 0)
        
        final_proxies['https'] = list(final_proxies['https'])
        final_proxies['http'] = list(final_proxies['http'])
        final_proxies['region'] = self.country_code
        return final_proxies

    def grab_proxy(self):
        proxies = self.__grab_proxy_list()
        return proxies

# ============================================================================================ #