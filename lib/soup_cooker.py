from bs4 import BeautifulSoup as bs
import requests

def get_property(soup, prop : str) -> (bool, str):
    std = str(soup)
    pos = std.find(prop)
    if pos == -1:
        return False, ""
    first_comma = std.find("\"", pos)
    last_comma = std.find("\"", first_comma + 1)
    value = std[first_comma + 1: last_comma]
    return True, value

def cook_soup(something):
    return bs(str(something), "html.parser")

def has_tag(something, tag : str):
    string = str(something)
    length = len(tag)
    return string[:length] == tag

def remove_full_tag(value : str, full_tag : str):
    f = value.find(full_tag)
    if f == -1:
        return value
    return value[:f] + value[f + len(full_tag):]

def find_last_prev(string : str, symb : str, pos : int):
    for i in range(pos + 1):
        offset = pos - i
        if string[offset] == symb:
            return offset
    return -1

if __name__ == "__main__":
    pass