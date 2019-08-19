# !/usr/bin/env python
import time
from queue import Queue
from threading import Thread
import lxml
import requests
from lxml import html
from lxml.html import fromstring
from .proxychecker import ProxyChecker
from .country_proxy_grabber import ScrapeProxy
import sys

import asyncio


class ProxyGrabber():
    proxy_list=[]

    valid_country_codes = ['ALL','US','UK','DE']

    def __init__(
        self, 
        len_proxy_list = 10, 
        country_code = 'ALL', 
        timeout = 10, 
        to_json = True,
        ):
        self.len_proxy_list = len_proxy_list

        if country_code not in self.valid_country_codes:
            country_code = 'ALL'

        self.country_code = country_code
        self.timeout = timeout
        self.to_json = to_json
        self.final_proxies = {
            'http': set(),
            'https': set(),
            'region' : country_code
        }

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
        if self.country_code == "ALL":
            print("************STARTING TO SCRAPE PROXIES************")
            scraped_proxies_http, scraped_proxies_https = ScrapeProxy.proxy_scraper(country_code = self.country_code,
                                                                        scraped_http_length = total_http_checked,
                                                                        scraped_https_length = total_https_checked,
                                                                        required_http_len = remaining_len_http, 
                                                                        required_https_len = remaining_len_https,
                                                                        batch = 100
                                                                        )
            count_http = 0
            count_https = 0
            total_http_checked += len(scraped_proxies_http)
            total_https_checked += len(scraped_proxies_https)

            print('LEN OF HTTP SCRAPED: {}'.format(len(scraped_proxies_http)))
            print('LEN OF HTTPS SCRAPED: {}'.format(len(scraped_proxies_https)))

            limit = self.len_proxy_list

            for batch in range(0, len(scraped_proxies_http), limit * 5):
                if (len(self.final_proxies['http']) < self.len_proxy_list):
                    try:
                        checked_http = ProxyChecker.proxy_checker_http(list(scraped_proxies_http)[batch: batch+(limit * 5)], self.timeout)
                    except IndexError:
                        checked_http = ProxyChecker.proxy_checker_http(list(scraped_proxies_http)[batch:], self.timeout)

                    for proxy in checked_http:
                        if proxy and (len(self.final_proxies['http']) < self.len_proxy_list):
                            count_http += 1
                            self.final_proxies['http'].add(proxy)
                    
            for batch in range(0, len(scraped_proxies_https), 100):
                if (len(self.final_proxies['https']) < self.len_proxy_list):
                    try:
                        checked_https = ProxyChecker.proxy_checker_https(list(scraped_proxies_https)[batch: batch+(limit * 5)], self.timeout)
                    except IndexError:
                        checked_https = ProxyChecker.proxy_checker_https(list(scraped_proxies_https)[batch:], self.timeout)

                    for proxy in checked_https:
                        if proxy and (len(self.final_proxies['https']) < self.len_proxy_list):
                            count_https += 1
                            self.final_proxies['https'].add(proxy)

        else:
            # FOR ALL OTHER REGIONS
            scraped_proxies_http, scraped_proxies_https = ScrapeProxy.proxy_scraper(country_code = self.country_code,
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
                pass

            if len(final_proxies['http']) < self.len_proxy_list:
                for proxy in checked_http:
                    if proxy and (len(final_proxies['http']) < self.len_proxy_list):
                        count_http += 1
                        self.final_proxies['http'].add(proxy)

            if len(final_proxies['https']) < self.len_proxy_list:
                for proxy in checked_https:
                    if proxy and (len(final_proxies['https']) < self.len_proxy_list):
                        count_https += 1
                        self.final_proxies['https'].add(proxy)

            remaining_len_http = remaining_len_http - count_http
            remaining_len_https = remaining_len_https - count_https
            
            remaining_len_http = max(remaining_len_http, 0)
            remaining_len_https = max(remaining_len_https, 0)

        self.final_proxies['https'] = list(self.final_proxies['https'])
        self.final_proxies['http'] = list(self.final_proxies['http'])

        self.final_proxies['http'] = list(self.final_proxies['http'])
        self.final_proxies['https'] = list(self.final_proxies['https'])
        
        return self.final_proxies

    def grab_proxy(self):
        start = time.time()
        proxies = self.__grab_proxy_list()
        end = time.time()
        print('TIME IS ')
        print(end-start)
        return proxies

# ============================================================================================ #