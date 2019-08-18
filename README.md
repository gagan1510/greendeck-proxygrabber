greendeck-proxygrabber
---

*This package is developed by [Greendeck](https://www.greendeck.co/)*
### Install from pip
https://pypi.org/project/greendeck-proxygrabber/

```pip install greendeck-proxygrabber```

### How to use ?
##### import the library
```python
import greendeck_proxygrabber
```

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
* len_proxy_list = 10
* country_code = 'ALL'
* timeout = 2
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
How to build your own pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5