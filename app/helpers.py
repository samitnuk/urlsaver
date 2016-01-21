import requests

# without this will be received SNIMissingWarning for https sites
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

def get_html(url):
    # without User-agent from some https sites will be received 403
    response = requests.get(url, headers={'User-Agent': 'python'})
    return response.text


def get_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find('title').text
    return title

#/ FOR TESTS /---------------------------------------------------------------
def main():
    url = 'https://dmitryzuev.com/ru/sasha-fine-art-nude'
    print ""
    print get_title(get_html(url))
    print ""

if __name__ == '__main__':
    main()