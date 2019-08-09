# !/usr/bin/env python
import time
from queue import Queue
from threading import Thread

import lxml
import requests
from lxml import html
from lxml.html import fromstring
from multiprocessing.dummy import Pool as ThreadPool
import asyncio
from grab import Grab, GrabError

headers = {
    "User-Agent": "Mozilla/5.0"
}

IP_CHECK_HTTPS = "https://api.ipify.org"
IP_CHECK_HTTP = "http://api.ipify.org"

class ProxyChecker:

    @classmethod
    def check_ip(cls, tup):
        proxy_value = tup[0]
        timeout = tup[1]
        g = Grab()
        try:
            
            if 'https' in list(proxy_value.keys()):
                g.setup(proxy=proxy_value['https'], proxy_type='https', connect_timeout=timeout, timeout=timeout)
                g.go('https://api.ipify.org')
                return proxy_value['https']
            
            else:
                g.setup(proxy=proxy_value['http'], proxy_type='http', connect_timeout=timeout, timeout=timeout)
                g.go('http://api.ipify.org')
                return proxy_value['http']

        except Exception as e:
            print(e)
            pass

    @classmethod
    def get_external_ip(cls, tup):
        proxy_value = tup[0]
        timeout = tup[1]
        try:
            if 'https' in list(proxy_value.keys()):
                r = requests.get(IP_CHECK_HTTPS, proxies=proxy_value, headers=headers, timeout=timeout)
                if r.text == proxy_value['https'].split('https://')[-1].split(':')[0]:
                    return proxy_value['https'].split('https://')[-1]
            else:
                r = requests.get(IP_CHECK_HTTP, proxies=proxy_value, headers=headers, timeout=timeout)
                if r.text == proxy_value['http'].split('http://')[-1].split(':')[0]:
                    return proxy_value['http'].split('http://')[-1]
        except IOError:
            return False

    @classmethod
    def proxy_checker_http(cls, proxy_list, timeout):
        try:
            final_proxy_list_http = []
            proxy_tuple_list_to_check = []
            if len(proxy_list):
                for proxy in list(proxy_list):
                    proxy_value = {
                        "http": "http://" + proxy
                    }
                    proxy_tuple_list_to_check.append((proxy_value, timeout))
            else:
                print('Not a valid list of proxies')

            pool = ThreadPool(50)
            final_proxy_list_http = pool.map(ProxyChecker.get_external_ip, proxy_tuple_list_to_check)
            # final_proxy_list_http = pool.map(ProxyChecker.check_ip, proxy_tuple_list_to_check)
            pool.close()
            pool.join()
            return final_proxy_list_http
        except Exception as e:
            print("INSIDE EXCEPTION!")
            print(e)
            return []

    @classmethod
    def proxy_checker_https(cls, proxy_list, timeout):
        try:
            proxy_tuple_list_to_check = []
            final_proxy_list_https = []
            if len(proxy_list):
                for proxy in list(proxy_list):
                    # print('Checking proxy: {}'.format(proxy))
                    proxy_value = {
                        "https": "https://" + proxy
                    }
                    proxy_tuple_list_to_check.append((proxy_value, timeout))
            else:
                print('Not a valid list of proxies')

            pool = ThreadPool(50)
            final_proxy_list_https = pool.map(ProxyChecker.get_external_ip, proxy_tuple_list_to_check)
            # final_proxy_list_https = pool.map(ProxyChecker.check_ip, proxy_tuple_list_to_check)
            pool.close()
            pool.join()
            return final_proxy_list_https
        except Exception as e:
            print("INSIDE EXCEPTION!")
            print(e)
            return []