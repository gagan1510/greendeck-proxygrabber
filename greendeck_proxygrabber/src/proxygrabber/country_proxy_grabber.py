import json
import requests
from lxml.html import fromstring
from . import constant

scraped_http_length = 0
scraped_https_length = 0

def proxy_scraper(
    country_code = 'ALL',
    scraped_http_length = 200,
    scraped_https_length = 200,
    required_http_len = 200, 
    required_https_len = 200,
    batch = 200
    ):

    proxies_http = set()
    proxies_https = set()
    COMBINED_COUNTRY_URL_HTTPS = constant.COMBINED_COUNTRY_URL_HTTP
    COMBINED_COUNTRY_URL_HTTP = constant.COMBINED_COUNTRY_URL_HTTPS

    # FOR COMBINED PROXIES
    if country_code == "ALL":
        # FOR HTTPS PROXIES
        if required_https_len > 0:
            https_response = requests.get(COMBINED_COUNTRY_URL_HTTPS[0])
            combined_proxies = json.loads(https_response.text)
            if (scraped_http_length+batch) < len(combined_proxies[0]['LISTA']):
                try:
                    for item in combined_proxies[0]['LISTA'][scraped_https_length : scraped_https_length + batch]:
                        proxies_https.add(
                            ':'.join([item['IP'], item['PORT']])
                        )
                        required_https_len -= 1
                except Exception as e:
                    print(e)
                    print("Exception Occured")
                    return None, None
                else:
                    pass

            if required_https_len > 0:
                response = requests.get(COMBINED_COUNTRY_URL_HTTPS[1])
                parser = fromstring(response.text)
                try:
                    for i in parser.xpath('//tbody/tr')[:required_https_len]:
                        if i.xpath('.//td[7][contains(text(),"yes")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            required_https_len -= 1
                            proxies_https.add(proxy)
                except IndexError:
                    for i in parser.xpath('//tbody/tr')[:]:
                        if i.xpath('.//td[7][contains(text(),"yes")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            required_https_len -= 1
                            proxies_https.add(proxy)
            
            if required_https_len > 0:
                response = requests.get(COMBINED_COUNTRY_URL_HTTPS[2])
                parser = fromstring(response.text)
                ips = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[1]')
                ports = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[2]')
                try:
                    for i in range(len(parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div'))):
                        proxy = ':'.join([ips[i].text, ports[i].text])
                        required_https_len -= 1
                        proxies_https.add(proxy)
                except Exception as e:
                    print(e)
                    print("URL 3 ERROR")

        # FOR HTTP PROXIES
        if required_http_len > 0:
            http_response = requests.get(COMBINED_COUNTRY_URL_HTTP[0])
            combined_proxies = json.loads(http_response.text)
            if (scraped_http_length+batch) < len(combined_proxies[0]['LISTA']):
                try:
                    for item in combined_proxies[0]['LISTA'][scraped_http_length:scraped_http_length+batch]:
                        proxies_http.add(
                            ':'.join([item['IP'], item['PORT']])
                        )
                        required_http_len -= 1
                        scraped_http_length += 1
                except Exception as e:
                    print(e)
                    print("Exception Occured")
                    return None, None
                else:
                    pass

            if required_http_len > 0:
                response = requests.get(COMBINED_COUNTRY_URL_HTTP[1])
                parser = fromstring(response.text)
                try:
                    for i in parser.xpath('//tbody/tr')[:required_http_len]:
                        if i.xpath('.//td[7][contains(text(),"no")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            required_http_len -= 1
                            scraped_http_length += 1
                            proxies_http.add(proxy)
                except IndexError:
                    for i in parser.xpath('//tbody/tr')[:]:
                        if i.xpath('.//td[7][contains(text(),"no")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            proxies_http.add(proxy)
            
            if required_http_len > 0:
                response = requests.get(COMBINED_COUNTRY_URL_HTTP[2])
                parser = fromstring(response.text)
                ips = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[1]')
                ports = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[2]')
                try:
                    for i in range(len(parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div'))):
                        proxy = ':'.join([ips[i].text, ports[i].text])
                        required_http_len -= 1
                        scraped_http_length += 1
                        proxies_http.add(proxy)
                except Exception as e:
                    print(e)
                    print("URL 3 ERROR")
    return proxies_http, proxies_https