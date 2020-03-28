from lib.mylang import *

letters = ["a", "b", "v", "g", "d", "e", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "x", "c", "ch", "sh", "ssh", "eh", "yu", "ya"]


def get_letter_hrefs():
    base_link = "https://royallib.com/authors-"
    res = []
    for letter in letters:
        this_link = base_link + letter + ".html"
        res.append(this_link)
    return res




if __name__ == '__main__':
    print(get_letter_hrefs())
