import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

import selenium

# establishing session
s = requests.Session()
s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    })

def load_user_data(user_id, page, session):
    url = 'http://www.kinopoisk.ru/user/%d/votes/list/ord/date/page/%d/#list' % (user_id, page)
    request = session.get(url)
    return request.text

def contain_movies_data(text):
    soup = BeautifulSoup(text)
    film_list = soup.find('div', {'class': 'profileFilmsList'})
    return film_list is not None

ya_xml_path = "https://yandex.ru/search/xml?user=lvv-2003&key=03.195052229:15b4cdde7ff532f1a4b3c8db5703e842"
ip = "91.122.140.80"

auth_url = "https://passport.yandex.ru/auth"
login = "lvv-2003@yandex.ru"
password = "pt598t6x"
# print(BeautifulSoup(s.get("https://passport.yandex.ru/auth?uid=195052229", auth=(login, password)).content, "html.parser"))

payload = {
        "email": login,
        "password": password
}
# result = s.post(auth_url, data = payload, headers = dict(referer = auth_url))

result = s.get()
print(bs(result.content, "html.parser"))
print(BeautifulSoup(s.get("https://yandex.ru/search/?text=yandex%20search%20api%20python%203&lr=2").content, "html.parser"))

