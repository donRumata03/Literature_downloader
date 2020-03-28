import yandex_search


# https://yandex.ru/search/xml?user=lvv-2003&key=03.195052229:15b4cdde7ff532f1a4b3c8db5703e842

yandex = yandex_search.Yandex(api_user='lvv-2003@yandex.ru', api_key='pt598t6x')
print(yandex.search("котики википедия").items)