print("You are using Greendeck Proxygrabber library!")

# your package information
name = "greendeck_proxygrabber"
__version__ = "0.0.1"
author = "Gagan Singh"
author_email = "gaganpreet.gs007@gmail.com"
url = ""

# import sub packages
from .src.proxygrabber.proxygrabber import ProxyGrabberClass
from .src.proxygrabber.country_proxy_grabber import proxy_scraper
from .src.proxygrabber.proxychecker import ProxyChecker