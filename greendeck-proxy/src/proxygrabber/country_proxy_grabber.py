import json
import requests
from lxml.html import fromstring

scraped_http_length = 0
scraped_https_length = 0

def proxy_scraper(
    country_code,
    scraped_http_length,
    scraped_https_length,
    required_http_len, 
    required_https_len,
    batch = 200
    ):

    proxies_http = set()
    proxies_https = set()
    COMBINED_COUNTRY_URL_HTTPS = ['https://www.proxy-list.download/api/v0/get?l=en&t=https', 'https://free-proxy-list.net/uk-proxy.html']
    COMBINED_COUNTRY_URL_HTTP = ['https://www.proxy-list.download/api/v0/get?l=en&t=http', 'https://free-proxy-list.net/uk-proxy.html']

    # FOR COMBINED PROXIES
    if country_code == "ALL":
        # FOR HTTPS PROXIES
        if required_https_len > 0:
            https_response = requests.get(COMBINED_COUNTRY_URL_HTTPS[0])
            combined_proxies = json.loads(https_response.text)
            try:
                for item in combined_proxies[0]['LISTA'][scraped_https_length:scraped_https_length+batch]:
                    proxies_https.add(
                        ':'.join([item['IP'], item['PORT']])
                    )
                    required_https_len -= 1
                    scraped_https_length += 1
            except IndexError as e:
                response = requests.get(COMBINED_COUNTRY_URL_HTTPS[1])
                parser = fromstring(response.text)
                for i in parser.xpath('//tbody/tr')[:required_https_len]:
                    if i.xpath('.//td[7][contains(text(),"yes")]'):
                        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                        scraped_https_length += 1
                        proxies_https.add(proxy)
            except:
                print(e)
                print("Exception Occured")
                return None, None

        # FOR HTTP PROXIES
        if required_http_len > 0:
            http_response = requests.get(COMBINED_COUNTRY_URL_HTTP[0])
            combined_proxies = json.loads(http_response.text)
            try:
                for item in combined_proxies[0]['LISTA'][scraped_http_length:scraped_http_length+batch]:
                    proxies_http.add(
                        ':'.join([item['IP'], item['PORT']])
                    )
                    required_http_len -= 1
                    scraped_http_length += 1
            except IndexError:     
                response = requests.get(COMBINED_COUNTRY_URL_HTTP[1])
                parser = fromstring(response.text)
                for i in parser.xpath('//tbody/tr')[:required_https_len]:
                    if i.xpath('.//td[7][contains(text(),"no")]'):
                        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                        proxies_http.add(proxy)
            except:
                print(e)
                print("Exception Occured")
                return None, None
    return proxies_http, proxies_https