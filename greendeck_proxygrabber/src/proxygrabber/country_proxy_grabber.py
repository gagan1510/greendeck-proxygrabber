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
                # 'https://www.proxy-list.download/api/v0/get?l=en&t=https'
                https_response = requests.get(COMBINED_COUNTRY_URL_HTTPS[0])
                combined_proxies = json.loads(https_response.text)
                if (scraped_https_length+batch) < len(combined_proxies[0]['LISTA']):
                    for jumps in range(scraped_https_length, scraped_https_length+required_https_len, batch):
                        try:
                            for item in combined_proxies[0]['LISTA'][jumps : jumps + batch]:
                                # if (required_https_len) == 0:
                                #     break
                                proxies_https.add(
                                    ':'.join([item['IP'], item['PORT']])
                                )
                                required_https_len -= 1
                                scraped_https_length += 1
                        except Exception as e:
                            print(e)
                            print("Exception Occured")
                            return None, None
                
                if required_https_len > 0:
                    # 'https://free-proxy-list.net/uk-proxy.html'
                    response = requests.get(COMBINED_COUNTRY_URL_HTTPS[1])
                    parser = fromstring(response.text)
                    try:
                        for i in parser.xpath('//tbody/tr')[:required_https_len]:
                            # if (required_https_len) == 0:
                            #     break
                            if i.xpath('.//td[7][contains(text(),"yes")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                required_https_len -= 1
                                proxies_https.add(proxy)
                            else:
                                pass
                    except IndexError:
                        for i in parser.xpath('//tbody/tr')[:]:
                            # if (required_https_len) == 0:
                            #     break
                            if i.xpath('.//td[7][contains(text(),"yes")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                required_https_len -= 1
                                scraped_https_length+=1
                                proxies_https.add(proxy)
                            else:
                                pass
                    except:
                        pass
                
                if required_https_len > 0:
                    # 'https://www.duplichecker.com/free-proxy-list.php'
                    response = requests.get(COMBINED_COUNTRY_URL_HTTPS[2])
                    parser = fromstring(response.text)
                    ips = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[1]')
                    ports = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[2]')
                    try:
                        for i in range(len(parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div'))):
                            # if (required_https_len) == 0:
                            #     break
                            proxy = ':'.join([ips[i].text, ports[i].text])
                            required_https_len -= 1
                            scraped_http_length+=1
                            proxies_https.add(proxy)
                    except Exception as e:
                        print(e)
                        print("URL 3 ERROR")

            # FOR HTTP PROXIES
            if required_http_len > 0:
                # 'https://www.proxy-list.download/api/v0/get?l=en&t=http', 
                http_response = requests.get(COMBINED_COUNTRY_URL_HTTP[0])
                combined_proxies = json.loads(http_response.text)
                if (scraped_http_length+batch) < len(combined_proxies[0]['LISTA']):
                    for jumps in range(scraped_http_length, scraped_http_length+required_http_len, batch):
                        try:
                            for item in combined_proxies[0]['LISTA'][jumps : jumps + batch]:
                                # if (required_http_len) == 0:
                                #     break
                                proxies_http.add(
                                    ':'.join([item['IP'], item['PORT']])
                                )
                                required_http_len -= 1
                                scraped_http_length+=1
                        except Exception as e:
                            print(e)
                            print("Exception Occured")
                            return None, None
                        else:
                            pass

                if required_http_len > 0:
                    # 'https://free-proxy-list.net/uk-proxy.html'
                    response = requests.get(COMBINED_COUNTRY_URL_HTTP[1])
                    parser = fromstring(response.text)
                    try:
                        for i in parser.xpath('//tbody/tr')[:required_http_len]:
                            # if (required_http_len) == 0:
                            #     break
                            if i.xpath('.//td[7][contains(text(),"no")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                required_http_len -= 1
                                scraped_http_length += 1
                                proxies_http.add(proxy)
                    except IndexError:
                        for i in parser.xpath('//tbody/tr')[:]:
                            if (required_http_len) == 0:
                                break
                            if i.xpath('.//td[7][contains(text(),"no")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                proxies_http.add(proxy)
                                required_http_len -= 1
                                scraped_http_length += 1
                                proxies_http.add(proxy)

                if required_http_len > 0:
                    # 'https://www.duplichecker.com/free-proxy-list.php'
                    response = requests.get(COMBINED_COUNTRY_URL_HTTP[2])
                    parser = fromstring(response.text)
                    ips = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[1]')
                    ports = parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div/div[2]')
                    try:
                        for i in range(len(parser.xpath('/html/body/div[5]/div/div[1]/div[1]/form/div/div/div/div[2]/div'))):
                            # if (required_http_len) == 0:
                            #     break
                            proxy = ':'.join([ips[i].text, ports[i].text])
                            required_http_len -= 1
                            scraped_http_length += 1
                            proxies_http.add(proxy)
                    except Exception as e:
                        print(e)
                        print("URL 3 ERROR")
        ################################################ FOR COMBINED PROXIES    
        
        ################################################ FOR GERMANY PROXIES
        if country_code == "DE":
            DE_COUNTRY_URL_HTTP = constant.COMBINED_DE_URL_HTTP
            DE_COUNTRY_URL_HTTPS = constant.COMBINED_DE_URL_HTTPS
            # FOR HTTPS PROXIES
            if required_https_len > 0:
                # 'https://www.proxy-list.download/api/v0/get?l=en&t=https'
                https_response = requests.get(DE_COUNTRY_URL_HTTPS[0])
                combined_proxies = json.loads(https_response.text)
                if (scraped_https_length+batch) < len(combined_proxies[0]['LISTA']):
                    # for jumps in range(scraped_https_length, required_https_len, batch):
                    try:
                        for item in combined_proxies[0]['LISTA']:
                            if item['ISO'] == 'DE':
                                proxies_https.add(
                                    ':'.join([item['IP'], item['PORT']])
                                )
                                required_https_len -= 1
                                scraped_https_length += 1
                    except Exception as e:
                        print(e)
                        print("Exception Occured")
            
                if required_https_len > 0:
                    pass
                

            # FOR HTTP PROXIES
            if required_http_len > 0:
                # 'https://www.proxy-list.download/api/v0/get?l=en&t=https'
                http_response = requests.get(DE_COUNTRY_URL_HTTP[0])
                combined_proxies = json.loads(http_response.text)
                if (scraped_http_length+batch) < len(combined_proxies[0]['LISTA']):
                    # for jumps in range(scraped_http_length, required_http_len, batch):
                    try:
                        for item in combined_proxies[0]['LISTA']:
                            if item['ISO'] == 'DE':
                                proxies_http.add(
                                    ':'.join([item['IP'], item['PORT']])
                                )
                                required_http_len -= 1
                                scraped_http_length+=1
                    except Exception as e:
                        print(e)
                        print("Exception Occured")
                        return None, None
                    else:
                        pass
                if required_http_len > 0:
                    pass
        ################################################ FOR GERMANY PROXIES

        ################################################ FOR UK PROXIES
        if country_code == "UK":
            UK_COUNTRY_URL_HTTP = constant.COMBINED_UK_URL_HTTP
            UK_COUNTRY_URL_HTTPS = constant.COMBINED_UK_URL_HTTPS
            # FOR HTTPS PROXIES
            if required_https_len > 0:
                # 'https://www.proxy-list.download/api/v0/get?l=en&t=https'
                https_response = requests.get(UK_COUNTRY_URL_HTTPS[0])
                combined_proxies = json.loads(https_response.text)
                # if (scraped_https_length+batch) < len(combined_proxies[0]['LISTA']):
                try:
                    for item in combined_proxies[0]['LISTA']:
                        if item['ISO'] == 'GB':
                            proxies_https.add(
                                ':'.join([item['IP'], item['PORT']])
                            )
                            required_https_len -= 1
                            scraped_https_length += 1
                except Exception as e:
                    print(e)
                    print("Exception Occured")
                    return None, None

                # if required_https_len > 0:
                if True:
                    # 'https://free-proxy-list.net/uk-proxy.html'
                    response = requests.get(UK_COUNTRY_URL_HTTPS[1])
                    parser = fromstring(response.text)
                    try:
                        for i in parser.xpath('//tbody/tr')[:required_https_len]:
                            if i.xpath('.//td[7][contains(text(),"yes")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                required_https_len -= 1
                                scraped_https_length+=1
                                proxies_https.add(proxy)
                            else:
                                pass
                    except IndexError:
                        for i in parser.xpath('//tbody/tr')[:]:
                            if i.xpath('.//td[7][contains(text(),"yes")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                required_https_len -= 1
                                scraped_https_length+=1
                                proxies_https.add(proxy)
                            else:
                                pass
                    except:
                        pass
                

            # FOR HTTP PROXIES
            if required_http_len > 0:
                # 'https://www.proxy-list.download/api/v0/get?l=en&t=https'
                http_response = requests.get(UK_COUNTRY_URL_HTTP[0])
                combined_proxies = json.loads(http_response.text)
                # if (scraped_http_length+batch) < len(combined_proxies[0]['LISTA']):
                try:
                    for item in combined_proxies[0]['LISTA']:
                        if item['ISO'] == 'GB':
                            proxies_http.add(
                                ':'.join([item['IP'], item['PORT']])
                            )
                            required_http_len -= 1
                            scraped_http_length+=1
                except Exception as e:
                    print(e)
                    print("Exception Occured")
                    
                # if required_http_len > 0:
                if True:
                    # 'https://free-proxy-list.net/uk-proxy.html'
                    response = requests.get(UK_COUNTRY_URL_HTTP[1])
                    parser = fromstring(response.text)
                    try:
                        for i in parser.xpath('//tbody/tr')[:required_http_len]:
                            if i.xpath('.//td[7][contains(text(),"no")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                proxies_http.add(proxy)
                                required_http_len -= 1
                                scraped_http_length += 1
                    except IndexError:
                        for i in parser.xpath('//tbody/tr')[:]:
                            if i.xpath('.//td[7][contains(text(),"no")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                proxies_http.add(proxy)
                                required_http_len -= 1
                                scraped_http_length += 1
        ################################################ FOR UK PROXIES

        ################################################ FOR US PROXIES
        if country_code == "US":
            US_COUNTRY_URL_HTTP = constant.COMBINED_US_URL_HTTP
            US_COUNTRY_URL_HTTPS = constant.COMBINED_US_URL_HTTPS

            # FOR HTTPS PROXIES
            if required_https_len > 0:
                # 'https://www.proxy-list.download/api/v0/get?l=en&t=https'
                https_response = requests.get(US_COUNTRY_URL_HTTPS[0])
                combined_proxies = json.loads(https_response.text)
                try:
                    for item in combined_proxies[0]['LISTA']:
                        if item['ISO'] == 'US':
                            proxies_https.add(
                                ':'.join([item['IP'], item['PORT']])
                            )
                            required_https_len -= 1
                            scraped_https_length += 1
                except Exception as e:
                    print(e)
                    print("Exception Occured")
                    return None, None
                if required_https_len > 0:
                    # 'https://www.us-proxy.org/'
                    response = requests.get(US_COUNTRY_URL_HTTPS[1])
                    parser = fromstring(response.text)
                    try:
                        for i in parser.xpath('//tbody/tr')[:required_https_len]:
                            if i.xpath('.//td[7][contains(text(),"yes")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                required_https_len -= 1
                                proxies_https.add(proxy)
                            else:
                                pass
                    except IndexError:
                        for i in parser.xpath('//tbody/tr')[:]:
                            if i.xpath('.//td[7][contains(text(),"yes")]'):
                                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                                required_https_len -= 1
                                scraped_https_length += 1
                                proxies_https.add(proxy)
                            else:
                                pass
                    except:
                        pass
                if required_https_len > 0:
                    # 'http://www.xroxy.com/proxy-country-US'
                    response = requests.get(US_COUNTRY_URL_HTTPS[2])
                    parser = fromstring(response.text)
                    try:
                        proxies = parser.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/text()')
                        ports = parser.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[2]/text()')
                        for i in range(required_https_len):
                            proxy = ':'.join([proxies[i], ports[i]])
                            required_https_len -= 1
                            scraped_https_length += 1
                            proxies_https.add(proxy)
                    except:
                        pass
            
            # FOR HTTP PROXIES
            if required_http_len > 0:
                http_response = requests.get(US_COUNTRY_URL_HTTP[0])
                combined_proxies = json.loads(http_response.text)
                try:
                    for item in combined_proxies[0]['LISTA']:
                        if item['ISO'] == 'US':
                            proxies_http.add(
                                ':'.join([item['IP'], item['PORT']])
                            )
                            required_http_len -= 1
                            scraped_http_length+=1
                except Exception as e:
                    print(e)
                    print("Exception Occured")
                    return None, None
                else:
                    pass
                
                if required_http_len > 0:
                    # 'https://www.us-proxy.org/'
                    response = requests.get(US_COUNTRY_URL_HTTP[1])
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
                                required_http_len -= 1
                                scraped_http_length += 1
                                proxies_http.add(proxy)
                if required_http_len > 0:
                    # 'http://www.xroxy.com/proxy-country-US'
                    response = requests.get(US_COUNTRY_URL_HTTPS[2])
                    parser = fromstring(response.text)
                    try:
                        proxies = parser.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[1]/text()')
                        ports = parser.xpath('//*[@id="DataTables_Table_0"]/tbody/tr/td[2]/text()')
                        for i in range(required_https_len):
                            proxy = ':'.join([proxies[i], ports[i]])
                            required_https_len -= 1
                            scraped_https_length += 1
                            proxies_https.add(proxy)
                    except:
                        pass
        ################################################ FOR US PROXIES
        
        return proxies_http, proxies_https