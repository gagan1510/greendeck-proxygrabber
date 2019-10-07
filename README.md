greendeck-proxygrabber 🎭
---
![Gd Logo](https://www.greendeck.co/images/logo/logo_full.png "Greenddeck")

*This package is developed by [Greendeck](https://www.greendeck.co/)*
### Install from pip
https://pypi.org/project/greendeck-proxygrabber/

```pip install greendeck-proxygrabber```

---
**WHATS NEW?**

Added proxy grabbing support of 4 new regions to proxy service, proxy grabber and proxy scraper.

---

### 👉 What is proxy service?

Proxy service is a service that keeps and updates a Mongo Database with latest up and running proxies.

### 👉 How to use?

##### import the service class

```python
from greendeck_proxygrabber import ProxyService
service = ProxyService(MONGO_URI = 'mongodb://127.0.0.1:27017',
                       update_time = 300,
                       pool_limit = 1000,
                       update_count = 200,
                       database_name = 'proxy_pool',
                       collection_name_http = 'http',
                       collection_name_https = 'https',
                       country_code = 'ALL'
                       )
```

This creates a service object.

##### Args

* update_time = Time after which proxies will be updated (in seconds)
* pool_limit = Limit after which insertion will change to updating
* update_count = Number of proxies to request grabber at a time
* database_name = Mongo Database name to store proxies in
* collection_name_http = Collection name to store http proxies in
* collection_name_https = Collection name to store https proxies in
* country_code = ISO code of one of regions supported

List of supported regions is:
* Combined Regions: ALL
* United States: US
* Germany: DE
* Great Britain: GB
* France: FR
* Czech Republic: CZ
* Netherlands: NL
* India: IN

#### Starting the service

```python
service.start()
```

Starting service gives the following output:

```Starting proxy service with the following configuration
MONGO_URI: mongodb://127.0.0.1:27017
Database: proxy_pool
Collection names: http, https
Press Ctrl+C once to stop...
Running Proxy Service...
```

This will run forever and will push/update proxies in mongodb after every {```update_time```} seconds.

### 👉 What is proxy to mongo?

Proxy to mongo is a functionality that lets you grab a set of valid proxies from the Internet and store it to the desired MongoDB database. You can schedule this to update or insert a given set of proxies to your database of pool, i.e. put it on airflow or any task scheduler.

### 👉 How to use?

##### import the ProxyToMongo class

```python
from greendeck_proxygrabber import ProxyService
service = ProxyToMongo( MONGO_URI = MONGO_URI,
                        pool_limit = 1000,
                        length_proxy = 200,
                        database_name='proxy_pool',
                        collection_name_http='http',
                        collection_name_https='https',
                        country_code='DE'
                        )
```

This creates a service object.

##### Args

* pool_limit = Total number of proxies to keep in mongo/pass None if you don't want to update
* length_proxy = Number of proxies to fetch at once
* database_name = Mongo Database name to store proxies in
* collection_name_http = Collection name to store http proxies in
* collection_name_https = Collection name to store https proxies in
* country_code = ISO code of one of regions supported

List of supported regions is:
* Combined Regions: ALL
* United States: US
* Germany: DE
* Great Britain: GB
* France: FR
* Czech Republic: CZ
* Netherlands: NL
* India: IN

#### Calling the ProxyToMongo grabber

```python
service.get_quick_proxy()
```

Starting Grabber gives the following output:

```Gathering proxies with the following configuration:
MONGO_URI: mongodb://127.0.0.1:27017
Database: proxy_pool
Collection names: http, https
Press Ctrl+C once to stop...
Running Proxy Grabber...
```

This will run forever and will push/update proxies in mongodb after every {```update_time```} seconds.

### 👉 How to use Proxy Grabber Class?

##### import ```ProxyGrabber``` class
```python
from greendeck_proxygrabber import ProxyGrabber
```

##### initialize ```ProxyGrabber``` object
```python
grabber = ProxyGrabber(len_proxy_list, country_code, timeout)
```
Here default values of some arguments are,
```
len_proxy_list = 10
country_code = 'ALL'
timeout = 2
```
Currently the program only supports proxies of combined regions

##### Getting checked, running proxies
The grab_proxy ```grab_proxy()``` function helps to fetch the proxies.
```python
grabber.grab_proxy()
```
This returns a dictionary of the following structure:
```python
{
    'https': [< list of https proxies >],
    'http': [< list of http proxies >],
    'region': 'ALL' # default for now
}
```
##### Getting an unchecked list of proxies
The grab_proxy ```proxy_scraper()``` method of ```ScrapeProxy``` helps to fetch the proxies.
This returns a list of 200 proxies of both type http and https.
```python
from greendeck_proxygrabber import ScrapeProxy
proxies_http, proxies_https = ScrapeProxy.proxy_scraper()
```
This returns list of proxies of type http proxies followed by https proxies.
```
http_proxies = [< list of http proxies >]
https_proxies = [< list of https proxies >]
```
##### Filtering invalid proxies from a list of proxies
The ```proxy_checker_https``` and ```proxy_checker_http``` methods from ```ProxyChecker``` class helps to validate the proxies.

Given a list of proxies, it checks each of them to be valid or not, and returns a list of valid proxies from the proxies feeded to it.

```python
from greendeck_proxygrabber import ProxyChecker
valid_proxies_http = ProxyChecker.proxy_checker_http(proxy_list = proxy_list_http, timeout = 2)
valid_proxies_https = ProxyChecker.proxy_checker_https(proxy_list = proxy_list_https, timeout = 2)
```

---
👉 How to build your own pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5
