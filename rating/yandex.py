import requests
from bs4 import BeautifulSoup as bs

def search(query, site = None):
    res = []

    url = "https://yandex.ru/search/?text=" + query + ("" if site is None else "&site=" + site)
    response = requests.get(url).text
    print(response)

    soup = bs(response, "html.parser")
    if len(soup.find_all('div', class_="main__content")) == 0:
        return []
    data = bs(str(soup.find('div', class_="main__content")), "html.parser")
    new_data = data.find_all('li', class_="serp-item")
    for li in new_data:
        buff = bs(str(li), "html.parser")
        all_buff = bs(str(buff.find_all('h2')[0]), "html.parser")
        ass = all_buff.find_all('a')
        for a in ass:
            if site is None or a.get("href").find(site) != -1:
                res.append(a.get("href"))
    return res


def search_data(query, site = None): # { Header, link, data }
    res = []
    url = "https://yandex.ru/search/?text=" + query + ("" if site is None else "&site=" + site)
    response = requests.get(url).text
    # print(response.encode('cp1251', 'ignore'))

    soup = bs(response, "html.parser")
    if len(soup.find_all('div', class_="main__content")) == 0:
        return []
    data = bs(str(soup.find('div', class_="main__content")), "html.parser")
    new_data = data.find_all('li', class_="serp-item")
    for li in new_data:
        buff = bs(str(li), "html.parser")
        header = bs(str(buff.find_all('h2')[0]), "html.parser")


    return res

def search_first(query, site = None, amount = 5):
    search_buff = search(query, site)
    search_result = search_buff if len(search_buff) < amount else search_buff[:amount]
    return search_result


def is_from_site(ref : str, site : str):
    s = ref.find(site)
    return s != -1 and s < 10


if __name__ == "__main__":
    refs = search("лев толстой", "wikipedia.org")
    print("\n".join(refs))