# !/usr/bin/env python
import time
from queue import Queue
from threading import Thread

import lxml
import requests
from lxml import html
from lxml.html import fromstring
from multiprocessing.dummy import Pool as ThreadPool

headers = {
    "User-Agent": "Mozilla/5.0"
}

IP_CHECK_HTTPS = "https://api.ipify.org"
IP_CHECK_HTTP = "http://api.ipify.org"

def get_external_ip(tup):
    proxy_value = tup[0]
    timeout = tup[1]
    try:
        if 'https' in list(proxy_value.keys()):
            r = requests.get(IP_CHECK_HTTPS, proxies=proxy_value, headers=headers, timeout=timeout)
            if r.text == proxy_value['https'].split('https://')[-1].split(':')[0]:
                return proxy_value['https'].split('https://')[-1]
            # else:
            #     print('NOT WORKING')
            #     print(proxy_value)

        else:
            r = requests.get(IP_CHECK_HTTP, proxies=proxy_value, headers=headers, timeout=timeout)
            if r.text == proxy_value['http'].split('http://')[-1].split(':')[0]:
                return proxy_value['http'].split('http://')[-1]
            # else:
            #     print('NOT WORKING')
            #     print(proxy_value)

    except IOError:
        return False
    except:
        return False

class ProxyChecker:
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
                pass
                # print('Not a valid list of proxies')

            # print('http proxies are being checked.')
            pool = ThreadPool(100)
            final_proxy_list_http = pool.map(get_external_ip, proxy_tuple_list_to_check)
            pool.close()
            pool.join()
            # print('http proxies checked.')
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
                    proxy_value = {
                        "https": "https://" + proxy
                    }
                    proxy_tuple_list_to_check.append((proxy_value, timeout))
            else:
                pass
                # print('Not a valid list of proxies')
            # print('https proxies are being checked.')
            pool = ThreadPool(100)
            final_proxy_list_https = pool.map(get_external_ip, proxy_tuple_list_to_check)
            pool.close()
            pool.join()
           
            # print('https proxies checked.')
            return final_proxy_list_https
        except Exception as e:
            print("INSIDE EXCEPTION!")
            print(e)
            return []