from lib.mylang import *
from royal_parsing.author_link_pages_getter import get_letter_hrefs
import requests
from bs4 import BeautifulSoup as bs

def load_author_page_links(hrefs : List[str]) -> dict:
    res = {}
    for page_href in hrefs:
        page_data = requests.get(page_href)

        soap = bs(page_data.text, "html.parser")
        tables = soap.find_all('table', class_="navi")
        if len(tables) == 0:
            continue
        table = tables[0]

        for part in table:
            thing = bs(str(part), features="html.parser").recursiveChildGenerator()
            for next_part in thing:
                string = str(next_part)
                if (string[:2] == "<a") and string.find("href") != -1:
                    last_pos = string.find(">") - 1
                    beg_href_pos = string.find("\"") + 1
                    href = "https:" + string[beg_href_pos: last_pos]
                    name = string[last_pos + 2: -4].strip().split()
                    res[" ".join(name)] = href
        print_good_info(f"Page {page_href} processed!")
    return res


def launch_loading():
    file_to_write = "D:\\Projects\\Literature_downloading\\res\\author_page_links.json"
    author_pages = load_author_page_links(get_letter_hrefs())
    string_to_write = json.dumps(author_pages, indent=4, ensure_ascii=False)
    byte_string_to_write = string_to_write.encode("utf-8")

    open(file_to_write, "wb").write(byte_string_to_write)

def patch_link_page():
    page = "https://royallib.com/authors-p.html"
    res = load_author_page_links([page])
    print_good_info("Loaded!")
    filename = "D:\\Projects\\Literature_downloading\\res\\authors-p.json"

    all_filename = "D:\\Projects\\Literature_downloading\\res\\author_page_links.json"

    # to_utf8_json_file(res, filename)
    total_res = from_utf8_json_file(all_filename)
    for i in res:
        total_res[i] = res[i]

    to_utf8_json_file(total_res, all_filename)


def load_author_page_links_from_file() -> dict:
    filename = "D:\\Projects\\Literature_downloading\\res\\author_page_links.json"
    # return json.loads(open(filename, "rb").read().decode("utf8"))
    return from_utf8_json_file(filename)



if __name__ == '__main__':
    launch_loading()
    # patch_link_page()
    # print_as_json(load_author_page_links_from_file())
