# -*- coding: utf-8 -*-
import requests
# from requests.exceptions import ConnectionError
from urlparse import urlparse

# without this will be received SNIMissingWarning from https sites
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

def add_scheme(url):
    if urlparse(url).scheme:
        return url
    return "http://" + url

def url_exists(url):
    try:
        # without User-agent from some https sites will be received 403
        r = requests.head(add_scheme(url),
                          headers={'User-Agent': 'Flask'}, verify=False)
        return r.status_code #== requests.codes.ok # == 200
    except:
        return False

def get_title(url):
    r = requests.get(add_scheme(url),
                     headers={'User-Agent': 'Flask'}, verify=False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.title.text

#/ FOR TESTS /---------------------------------------------------------------
def main():
    urls = ['https://fantlab.ru/autor1667',
            'amlab.me/',
            'https://www.facebook.com/',
            'habrahabr.ru/post/150302/',
            "http://yummymommy.com.ua/post-2.html",
            "http://www.uz.gov.ua/",
            "sputniktv.in.ua/112-ukrana.html",
            "http://sweden.mfa.gov.ua/ua"]
    print
    for url in urls:    
        if url_exists(url):
            print get_title(url)
        else:
            print url_exists(url)

if __name__ == '__main__':
    main()
    

