# -*- coding: utf-8 -*-
import requests
# from requests.exceptions import ConnectionError
from urlparse import urlparse

# without this will be received SNIMissingWarning from https sites
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

def add_scheme(url):
    if urlparse(url).scheme:
        return url
    return "http://" + url

def url_exists(url):
    try:
        # without User-agent from some https sites will be received 403
        r = requests.head(add_scheme(url),
                          headers={'user-agent': user_agent}, verify=False)
        return r.status_code #== requests.codes.ok # == 200
    except:
        return False

def get_title(url):
    r = requests.get(add_scheme(url),
                     headers={'user-agent': user_agent}, verify=False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.title.text

#/ FOR TESTS /---------------------------------------------------------------
def main():
    urls = ['https://www.behance.net/gallery/18264987/Biotop-from-Polygonia']
    print
    for url in urls:    
        if url_exists(url):
            print '-->', get_title(url)
        else:
            print url_exists(url)
    print

if __name__ == '__main__':
    main()
    

