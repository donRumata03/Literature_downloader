import requests
from bs4 import BeautifulSoup as bs
import json

res_path = "../test_data.json"

start_path = "https://royallib.com/authors-"


hrefs = []
letters = ["a", "b", "v", "g", "d", "e", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "r", "s", "t", "u", "f", "x", "c", "ch", ]

test_letters = letters[:1]

for letter in test_letters:

    this_page_name = start_path + letter + ".html"
    print(this_page_name)
    page_data = requests.get(this_page_name)

    soap = bs(page_data.text, "html.parser")
    tables =soap.find_all('table', class_ = "navi") 
    table = tables[0]

    for part in table:
        thing = bs(str(part), features="html.parser").recursiveChildGenerator()
        for next_patr in thing:
            string = str(next_patr)
            if (string[:2] == "<a") and string.find("href") != -1:
                last_pos = string.find(">") - 1
                beg_href_pos = string.find("\"") + 1
                href = "https:" + string[beg_href_pos : last_pos]
                name = string[last_pos + 2 : -4].split()
                this_res = (name, href)
                hrefs.append(this_res)

file_to_write = open(res_path, "w")

string_to_write = json.dumps(hrefs)#.encode("utf8", "ignore")

print(hrefs[20])

file_to_write.write(string_to_write)
file_to_write.close()
