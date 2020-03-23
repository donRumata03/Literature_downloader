import yandex_search

yandex = yandex_search.Yandex(api_user='lvv-2003@yandex.ru', api_key='pt598t6x')
print(yandex.search('"Interactive Saudi"').items)