import json
import requests
from lxml.html import fromstring
from . import constant
import urllib

scraped_http_length = 0
scraped_https_length = 0

class ScrapeProxy():
    country_code_dict = {
        'Great Britain': 'UK',
        'United Kingdom': 'UK',
        'Germany': 'DE',
        'United States': 'US'
    }

    @classmethod
    def proxyz(
        cls,
        country_code = 'ALL',
        required_http_len = 200,
        required_https_len = 200,
        ):
        i = 0
        scraped_proxies = []
        while (len(scraped_proxies) <= required_http_len) or len(scraped_proxies) < required_http_len:
            url = 'http://www.proxz.com/proxy_list_high_anonymous_{}_ext.html'
            url = url.format(i)
            i += 1
            try:
                response = requests.get(url)
                selector = fromstring(response.text)
                for i in range(len(selector.xpath('/html/body/div/center//text()'))):
                    if 'eval' in selector.xpath('/html/body/div/center//text()')[i]:
                        if country_code == 'ALL':
                            scraped_proxies.append(
                                ':'.join(
                                    [
                                        urllib.parse.unquote(selector.xpath('/html/body/div/center//text()')[i][15:-4]).split('"')[-2],
                                        selector.xpath('/html/body/div/center//text()')[i+2]
                                ])
                            )
                        else:
                            if ScrapeProxy.country_code_dict[selector.xpath('/html/body/div/center//text()')[i+4]] == country_code:
                                scraped_proxies.append(
                                    ':'.join(
                                        [
                                            urllib.parse.unquote(selector.xpath('/html/body/div/center//text()')[i][15:-4]).split('"')[-2],
                                            selector.xpath('/html/body/div/center//text()')[i+2]
                                    ])
                                )
            except:
                return scraped_proxies

        return scraped_proxies

    @classmethod
    def proxy_scraper(
        cls,
        country_code = 'ALL',
        scraped_http_length = 0,
        scraped_https_length = 0,
        required_http_len = 200,
        required_https_len = 200,
        batch = 200
        ):

        proxies_http = set()
        proxies_https = set()

        ################################################ FOR COMBINED PROXIES
        if country_code == "ALL":
            COMBINED_COUNTRY_URL_HTTP = constant.COMBINED_COUNTRY_URL_HTTP
            COMBINED_COUNTRY_URL_HTTPS = constant.COMBINED_COUNTRY_URL_HTTPS
            # FOR HTTPS PROXIES
            if required_https_len > 0:
                try:
                    # 'https://www.proxy-list.download/api/v1/get?type=https&anon=elite'
                    https_response = requests.get(COMBINED_COUNTRY_URL_HTTPS[0])
                    combined_proxies = (https_response.text).split('\r\n')
                    try:
                        for item in combined_proxies:
                            proxies_https.add(item)
                            required_https_len -= 1
                            scraped_https_length += 1
                    except Exception as e:
                        print(e)
                        print("Exception Occured")
                        return None, None
                except Exception as e:
                    print(e)
                    pass

                scraped_https_length = max(0, scraped_https_length - len(combined_proxies))
                
                response = requests.get(COMBINED_COUNTRY_URL_HTTPS[4])
                try:
                    parser = response.text.split('\n')
                    for item in parser:
                        try:
                            item = eval(item)
                            if item['type'] == 'https':                            
                                proxies_https.add(
                                        ':'.join([str(item['host']), str(item['port'])])
                                    )
                        except:
                            pass
                except Exception as e:
                    print("YAHA 1")
                    print(e)

                response = requests.get(COMBINED_COUNTRY_URL_HTTPS[5])
                try:
                    parser = response.text.split('\n')
                    for item in parser:
                        try:
                            if len(item.split('|')) == 7:
                                if item.split('|')[3] == 'https':                            
                                    proxies_https.add(
                                            ':'.join([str(item.split('|')[1]), str(item.split('|')[2])])
                                    )
                        except:
                            pass
                except Exception as e:
                    print("YAHA 1")
                    print(e)
                # if required_https_len > 0:
                    # 'https://free-proxy-list.net/uk-proxy.html'
                response = requests.get(COMBINED_COUNTRY_URL_HTTPS[1])
                parser = fromstring(response.text)
                try:
                    for i in parser.xpath('//tbody/tr'):
                        # if (required_https_len) == 0:
                        #     break
                        if i.xpath('.//td[7][contains(text(),"yes")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                        else:
                            pass
                except IndexError:
                    for i in parser.xpath('//tbody/tr'):
                        if i.xpath('.//td[7][contains(text(),"yes")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            required_https_len -= 1
                            scraped_https_length+=1
                            proxies_https.add(proxy)
                        else:
                            pass
                except:
                    pass
                
                # 'https://www.duplichecker.com/free-proxy-list.php'
                response = requests.get(COMBINED_COUNTRY_URL_HTTPS[2])
                parser = fromstring(response.text)
                ips = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[1]')
                ports = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[2]')
                try:
                    for i in range(len(parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div'))):
                        proxy = ':'.join([ips[i].text, ports[i].text])
                        required_https_len -= 1
                        scraped_http_length+=1
                        proxies_https.add(proxy)
                except Exception as e:
                    print(e)
                    print("URL 3 ERROR")

                try:
                    # 'https://www.proxy-list.download/api/v1/get?type=https&anon=elite'
                    https_response = requests.get(COMBINED_COUNTRY_URL_HTTPS[3])
                    combined_proxies = (https_response.text).split('\n')
                    try:
                        for item in combined_proxies:
                            proxies_https.add(item)
                            required_https_len -= 1
                            scraped_https_length += 1
                    except Exception as e:
                        print(e)
                        print("Exception Occured")
                        return None, None
                except Exception as e:
                    print(e)
                    pass

            # FOR HTTP PROXIES
            if required_http_len > 0:
                # 'https://www.proxy-list.download/api/v1/get?type=http&anon=elite', 
                try:
                    http_response = requests.get(COMBINED_COUNTRY_URL_HTTP[0])
                    combined_proxies = (http_response.text).split('\r\n')
                    try:
                        for item in combined_proxies:
                            proxies_http.add(item)
                    except Exception as e:
                        print(e)
                        print("Exception Occured")
                        return None, None
                    else:
                        pass
                except Exception as e: 
                    print(e)
                
                scraped_http_length = max(0, scraped_http_length - len(combined_proxies))

                response = requests.get(COMBINED_COUNTRY_URL_HTTP[4])
                try:
                    parser = response.text.split('\n')
                    for item in parser:
                        try:
                            item = eval(item)
                            if item['type'] == 'http':
                                proxies_http.add(
                                        ':'.join([str(item['host']), str(item['port'])])
                                    )
                        except:
                            pass
                except Exception as e:
                    print("YAHA 2")
                    print(e)
                
                response = requests.get(COMBINED_COUNTRY_URL_HTTP[5])
                try:
                    parser = response.text.split('\n')
                    for item in parser:
                        try:
                            if len(item.split('|')) == 7:
                                if item.split('|')[3] == 'https':                            
                                    proxies_http.add(
                                            ':'.join([str(item.split('|')[1]), str(item.split('|')[2])])
                                    )
                        except:
                            pass
                except:
                    pass
                response = requests.get(COMBINED_COUNTRY_URL_HTTP[1])
                parser = fromstring(response.text)
                scraped_http_length -= len(parser.xpath('//tbody/tr'))
                try:
                    for i in parser.xpath('//tbody/tr'):
                        if i.xpath('.//td[7][contains(text(),"no")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            required_http_len -= 1
                            scraped_http_length += 1
                            proxies_http.add(proxy)
                except IndexError:
                    for i in parser.xpath('//tbody/tr'):
                        if i.xpath('.//td[7][contains(text(),"no")]'):
                            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                            proxies_http.add(proxy)
                            required_http_len -= 1
                            scraped_http_length += 1
                            proxies_http.add(proxy)


                # 'https://www.duplichecker.com/free-proxy-list.php'
                response = requests.get(COMBINED_COUNTRY_URL_HTTP[2])
                parser = fromstring(response.text)
                ips = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[1]')
                ports = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[2]')
                try:
                    for i in range(len(parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div'))):
                        proxy = ':'.join([ips[i].text, ports[i].text])
                        proxies_http.add(proxy)
                except Exception as e:
                    print(e)
                    print("URL 3 ERROR")
                
                try:
                    http_response = requests.get(COMBINED_COUNTRY_URL_HTTP[3])
                    combined_proxies = (http_response.text).split('\n')
                    try:
                        for item in combined_proxies:
                            proxies_http.add(item)
                    except Exception as e:
                        print(e)
                        print("Exception Occured")
                        return None, None
                    else:
                        pass
                except:
                    pass
                
        ################################################ FOR COMBINED PROXIES    
        
        return proxies_http, proxies_https