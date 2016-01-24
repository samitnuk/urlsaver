import requests
from requests.exceptions import ConnectionError

# without this will be received SNIMissingWarning from https sites
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

def get_html(url):
    # without User-agent from some https sites will be received 403
    response = requests.get(url,headers={'User-Agent': 'python'},
                            verify=False)
    return response.text

def url_validator(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'python'},
                                verify=False)
        return response.status_code == 200
    except ConnectionError:
        return False

def get_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find('title').text
    return title

def get_path(path, groupname=""):
    pass

#/ FOR TESTS /---------------------------------------------------------------
def main():
    url = 'https://fantlab.ru/autor1667'
    print ""
    print url_validator(url)
    print get_title(get_html(url))
    print ""

if __name__ == '__main__':
    main()