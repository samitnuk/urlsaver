import requests
from requests.exceptions import ConnectionError

# without this will be received SNIMissingWarning from https sites
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

def url_exists(url):
    try:
        # without User-agent from some https sites will be received 403
        r = requests.head(url, headers={'User-Agent': 'Flask'}, verify=False)
        return r.status_code == requests.codes.ok # == 200
    except ConnectionError:
        return False

def get_title(url):
    r = requests.get(url, headers={'User-Agent': 'Flask'}, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find('title').text

#/ FOR TESTS /---------------------------------------------------------------
def main():
    url = 'https://fantlab.ru/autor1667'
    print ""
    if url_exists(url):
        print get_title(url)
    else:
        print url_exists(url)

if __name__ == '__main__':
    main()