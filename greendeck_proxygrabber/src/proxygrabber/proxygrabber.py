# !/usr/bin/env python
import sys
import time
import threading
from queue import Queue
import lxml
import requests
from lxml import html
from lxml.html import fromstring
from .proxychecker import ProxyChecker
from .country_proxy_grabber import ScrapeProxy
import sys
import pymongo

import asyncio

# ============================================================================================ #
class ProxyGrabber():
    proxy_list=[]
    valid_country_codes = ['ALL','US','GB','DE', 'FR']
    def __init__(
        self,
        len_proxy_list = 10,
        country_code = 'ALL',
        timeout = 10,
        ):
        self.len_proxy_list = len_proxy_list

        if country_code.upper() not in self.valid_country_codes:
            country_code = 'ALL'

        self.country_code = country_code.upper()
        self.timeout = timeout
        self.final_proxies = {
            'http': set(),
            'https': set(),
            'region' : country_code
        }

    def __grab_proxy_list(self):
        total_http_checked = 0
        total_https_checked = 0
        remaining_len_http = self.len_proxy_list
        remaining_len_https = self.len_proxy_list
        self.final_proxies['http'] = set()
        self.final_proxies['https'] = set()

        # FOR COMBINED REGIONS
        if self.country_code == "ALL":
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
            
            self.final_proxies['https'] = list(self.final_proxies['https'])
            self.final_proxies['http'] = list(self.final_proxies['http'])
        
        # FOR SINGLE REGION
        else:
            scraped_proxies_http, scraped_proxies_https = ScrapeProxy.proxy_scraper(country_code = self.country_code,
                                                                        scraped_http_length = total_http_checked,
                                                                        scraped_https_length = total_https_checked,
                                                                        required_http_len = remaining_len_http, 
                                                                        required_https_len = remaining_len_https,
                                                                        batch = 50
                                                                        )
            
            count_http = 0
            count_https = 0
            total_http_checked += len(scraped_proxies_http)
            total_https_checked += len(scraped_proxies_https)

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
            
            self.final_proxies['https'] = list(self.final_proxies['https'])
            self.final_proxies['http'] = list(self.final_proxies['http'])

        return self.final_proxies

    def grab_proxy(self):
        proxies = self.__grab_proxy_list()
        end = time.time()
        return proxies

# ============================================================================================ #
class ProxyService():
    def __init__(
        self,
        MONGO_URI = 'mongodb://127.0.0.1:27017',
        update_time = 300,
        pool_limit = 1000,
        update_count = 200,
        database_name = 'proxy_pool',
        collection_name_http = 'http',
        collection_name_https = 'https',
        country_code = 'ALL'
        ):
        if type(MONGO_URI) == type(' '):
            self.MONGO_URI = MONGO_URI
        else:
            raise TypeError
        
        if type(country_code) == type(' '):
            self.country_code = country_code.upper()
        else:
            raise TypeError

        if type(database_name) == type(' '):
            self.database_name = database_name
        else:
            raise TypeError

        if type(collection_name_http) == type(' '):
            self.collection_name_http = collection_name_http
        else:
            raise TypeError

        if type(collection_name_https) == type(' '):
            self.collection_name_https = collection_name_https
        else:
            raise TypeError

        if type(update_count) == type(2):
            self.update_count = update_count
        else:
            raise TypeError

        if type(update_time) == type(2):
            self.update_time = update_time
        else:
            raise TypeError

        if type(pool_limit) == type(2):
            self.pool_limit = pool_limit
        else:
            raise TypeError

        self.information = '''Starting proxy service with the following configuration\nMONGO_URI: {}\nDatabase: {}\nCollection names: {}, {}\nPress Ctrl+C to stop...'''.format(self.MONGO_URI, self.database_name, self.collection_name_http, self.collection_name_https)
        self.delay = 0.01
    
    def __proxy_service(self):
        grabber = ProxyGrabber(len_proxy_list=self.update_count, country_code=self.country_code)
        while True:
            sys.stdout.write('\nRunning Proxy Service...')
        
            proxies = grabber.grab_proxy()
            try:
                client = pymongo.MongoClient(
                    self.MONGO_URI
                )
            except:
                continue
            db = client[self.database_name]
            collection_http = db[self.collection_name_http]
            collection_https = db[self.collection_name_https]            
            start = time.time()
            
            # INSERTING HTTP PROXIES
            http = []
            for item in proxies['http']:
                proxy = {
                    'http' : 'http://{}'.format(item)
                }
                http.append(proxy)
        
            collection_http.insert_many(http)
        
            # INSERTING HTTPS PROXIES
            https = []
            for item in proxies['https']:
                proxy = {
                    'https' : 'https://{}'.format(item)
                }
                https.append(proxy)
        
            collection_https.insert_many(https)
        
            if collection_http.count() >= self.pool_limit:
                http_to_remove = collection_http.find({}, {'_id': 1}).limit(self.update_count)
                http_to_remove = [http_proxy['_id'] for http_proxy in http_to_remove]
                collection_http.remove({'_id': {'$in': http_to_remove}})
            
            if collection_https.count() >= self.pool_limit:
                https_to_remove = collection_https.find({}, {'_id': 1}).limit(self.update_count)
                https_to_remove = [https_proxy['_id'] for https_proxy in https_to_remove]
                collection_https.remove({'_id': {'$in': https_to_remove}})


            client.close()
            end = time.time()
            time.sleep(max(0, (self.update_time - (end - start))))
            sys.stdout.write('\b')

        print("Proxies Updated!")
                
    def start(self):
        for i in self.information:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(self.delay)
        self.__proxy_service()

# ============================================================================================ #
class ProxyToMongo():
    def __init__(
        self,
        MONGO_URI = 'mongodb://127.0.0.1:27017',
        pool_limit = 1000,
        length_proxy = 200,
        database_name = 'proxy_pool',
        collection_name_http = 'http',
        collection_name_https = 'https',
        country_code = 'ALL'
        ):
        if type(MONGO_URI) == type(' '):
            self.MONGO_URI = MONGO_URI
        else:
            raise TypeError
        
        if type(country_code) == type(' '):
            self.country_code = country_code.upper()
        else:
            raise TypeError

        if type(database_name) == type(' '):
            self.database_name = database_name
        else:
            raise TypeError

        if type(collection_name_http) == type(' '):
            self.collection_name_http = collection_name_http
        else:
            raise TypeError

        if type(collection_name_https) == type(' '):
            self.collection_name_https = collection_name_https
        else:
            raise TypeError
        
        if type(pool_limit) == type(2):
            self.pool_limit = pool_limit
        elif type(pool_limit) == type(None):
            self.pool_limit = pool_limit
        else:
            raise TypeError

        if type(length_proxy) == type(2):
            self.length_proxy = length_proxy
        else:
            raise TypeError

        self.information = '''Gathering proxies with the following configuration:\nMONGO_URI: {}\nDatabase: {}\nCollection names: {}, {}\nPress Ctrl+C to stop...'''.format(self.MONGO_URI, self.database_name, self.collection_name_http, self.collection_name_https)
        self.delay = 0.01
    
    def __gather_proxy(self):
        grabber = ProxyGrabber(len_proxy_list=self.length_proxy, country_code=self.country_code)
        print('\nRunning Proxy Grabber...')
        proxies = grabber.grab_proxy()
        try:
            client = pymongo.MongoClient(
                self.MONGO_URI
            )
        except:
            return
        db = client[self.database_name]
        collection_http = db[self.collection_name_http]
        collection_https = db[self.collection_name_https]            
        start = time.time()
        
        # INSERTING HTTP PROXIES
        http = []
        for item in proxies['http']:
            proxy = {
                'http' : 'http://{}'.format(item)
            }
            http.append(proxy)
    
        collection_http.insert_many(http)
    
        # INSERTING HTTPS PROXIES
        https = []
        for item in proxies['https']:
            proxy = {
                'https' : 'https://{}'.format(item)
            }
            https.append(proxy)
    
        collection_https.insert_many(https)

        if type(self.pool_limit) == type(1):
            if collection_http.count() >= self.pool_limit:
                http_to_remove = collection_http.find({}, {'_id': 1}).limit(int(collection_http.count()) - self.pool_limit)
                http_to_remove = [http_proxy['_id'] for http_proxy in http_to_remove]
                collection_http.remove({'_id': {'$in': http_to_remove}})
            
            if collection_https.count() >= self.pool_limit:
                https_to_remove = collection_https.find({}, {'_id': 1}).limit(int(collection_http.count()) - self.pool_limit)
                https_to_remove = [https_proxy['_id'] for https_proxy in https_to_remove]
                collection_https.remove({'_id': {'$in': https_to_remove}})
        else:
            pass

        client.close()
        end = time.time()

        print('\b')
        print("Proxies Grabbed!")
                
    def get_quick_proxy(self):
        for i in self.information:
            print(i)
            time.sleep(self.delay)
        self.__gather_proxy()