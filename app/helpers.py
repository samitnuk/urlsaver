import requests
from requests.exceptions import ConnectionError
from urlparse import urlparse

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

def is_correct_path(path):
    o = urlparse(path)
    return o.scheme, o.netloc


#/ FOR TESTS /---------------------------------------------------------------
def main():
    url = 'https://fantlab.ru/autor1667'
    # url = '//my/name'
    print
    # if url_exists(url):
    #     print get_title(url)
    # else:
    #     print url_exists(url)
    print is_correct_path(url)

if __name__ == '__main__':
    main()

#/ WILL BE REMOVED /---------------------------------------------------------
from urlparse import urlparse

@app.route("/")
@app.route("/<path:path>")
def main(path=None):
    if path:
        if urlparse(path).scheme and url_exists(path):
            if current_user.is_authenticated:
                save_url(path, ''))
                return redirect(url_for('main'))
            session['url'] = path
            return redirect(url_for('login'))
        return redirect(url_for('main'))
    if session['url']:
        save_url(session['url'], getattr(session, 'groupname', ''))
        session['url'], session['groupname'] = '', ''
        return redirect(url_for('main'))
    else:
        if current_user.is_authenticated:
            urls = db.session.query(Locator)\
                .filter_by(username=current_user.username).all()
            return render_template('urls.html', urls=urls)
        return render_template('home.html')

def save_url(path, groupname):
    locator = Locator(url=path, title=get_title(path),
                      groupname=groupname, date=datetime.today(),
                      username=current_user.username)
    db.session.add(locator)
    db.session.commit()
    # return