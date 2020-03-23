import time

from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup as bs
import soup_cooker
from soup_cooker import get_property
import json
from mylang import Vova
import rater
import wikipedia
import mylang
import os
from mylang import *
import thread_loader

res_path = "test_data.txt"
start_path = "https://royallib.com/authors-"

letters = ["a", "b", "v", "g", "d", "e", "zh", "z", "i", "j", "k", "l", "m", "n", "o", "r", "s", "t", "u", "f", "x", "c", "ch", "sh", "ssh", "eh", "yu", "ya"]
min_acceptable_artwork_number = 10
min_acceptable_artwork_number_for_good_authors = 5
no_txt_limit = 5
autor_resave_limit = 20

def get_author_names_and_links(num : int = None):
    hrefs = []
    letter_index = 0
    for letter in letters:
        if num is not None and letter_index >= num:
            break
        this_page_name = start_path + letter + ".html"
        print(this_page_name)
        page_data = requests.get(this_page_name)

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
                    this_res = (name, href)
                    hrefs.append(this_res)
        letter_index += 1
    return hrefs


def get_author_books(ref) -> list:
    data = bs(requests.get(ref).text, "html.parser")
    content = data.find('div', class_ = "content")
    table = bs(str(bs(str(content), "html.parser").find('table')), "html.parser")
    res = []
    for td in table.recursiveChildGenerator():
        std = str(td)
        good_td = bs(std, "html.parser")
        title_pos = std.find("title")
        if std[:2] != "<a" or title_pos == -1:
            continue
        first_comma = std.find("\"", title_pos)
        last_comma = std.find("\"", first_comma + 1)
        title = std[first_comma + 1 : last_comma]
        if title == "Скачать книгу":
            res.append({"name" : good_td.text, "link" : "https:" + get_property(good_td, "href")[1]})

    return res


def get_download_href(page : str):
    data = bs(str(requests.get(page).text), "html.parser")
    refs = data.find_all('a')
    for ref in refs:
        if ref.text == "Скачать в формате TXT":
            href_prop = get_property(ref, "href")
            if href_prop[0]:
                return "https:" + href_prop[1]
    print("No txt file for " + page)
    raise Exception("No txt file!")


def get_artwork_data(artwork_content : bs) -> dict: # {name, genre, link... }
    string = str(artwork_content)
    res = {}
    prop_names_converter = {"Автор" : "author", "Название" : "name", "Жанр" : "genre"}

    all_tables = artwork_content.find_all('table')
    table = None
    for poss_table in all_tables:
        # cellspacing = get_property(table_soup, "cellspacing")
        # cellpadding = get_property(table_soup, "cellpadding")
        # not cellspacing[0] or not cellpadding[0] or cellpadding[1] != "8px" or cellpadding[1] != "8px" or

        table = soup_cooker.cook_soup(str(poss_table))
        break
    if table is None:
        return {}

    table_index = 0
    for ch in table.recursiveChildGenerator():
        if soup_cooker.has_tag(ch, "<table"):
            if table_index:
                table = soup_cooker.cook_soup(ch)
                break
            else:
                table_index += 1

    tds = [soup_cooker.cook_soup(i) for i in table.find_all("td")]
    for td in tds:
        str_td = str(td)
        if str_td.find("<b>") == -1:
            continue
        raw_key = soup_cooker.cook_soup(td.find_all("b")[0])
        key = raw_key.text.strip()
        if key[-1] == ":":
            key = key[:-1]
        raw_value = soup_cooker.cook_soup(soup_cooker.remove_full_tag(str_td, str(raw_key)))
        value = raw_value.text.strip()
        res[key] = value

    hrefs = artwork_content.find_all("a")
    download_href = None
    href_body = ""
    for href in map(str, hrefs):
        pos = href.find("Скачать в формате TXT")
        if pos == -1:
            continue
        download_href = "https:" + get_property(href, "href")[1]
        href_body = href
    res["link"] = download_href
    if download_href is not None:
        size = count_byte_size(string[string.find(href_body) + href_body.__len__():])
        if size is not None:
            res["size"] = size

    total_res = res.copy()

    for i in res:
        if i in prop_names_converter:
            total_res[prop_names_converter[i]] = res[i]
    ''' 
    parent = None
    prev_parent = None
    for obj in table.recursiveChildGenerator():
        this_soup = soup_cooker.cook_soup(obj)
        if soup_cooker.has_tag(obj, "<b>"):
            prop_name = this_soup.text
            if prop_name in prop_names_converter:
                prop_name = prop_names_converter[prop_name]
            # print(prop_name, "Parent :",  str(prev_parent), False if len(prev_parent.strip()) != 0)
        else:
            prev_parent = parent
            parent = obj

            #print("Other data : ", other_data)
    '''
    return total_res


def make_all_data(max_recursive_counter = None):
    all_data = []
    recursive_counter = 0
    author_data = get_author_names_and_links()
    for author in author_data:
        print(" ".join(author[0]), " : ")
        literature = get_author_books(author[1])
        # print(" ,".join(literature)[0], "\n", " ,".join(literature)[1])
        print(literature)
        author_name = " ".join(author[0])
        author_data = {"name": author_name, "page": author[1], "artworks" : []}
        for artwork in literature:
            if max_recursive_counter is not None and recursive_counter >= max_recursive_counter:
                return all_data
            artwork_data = {"name" : artwork[0], "link" : None}
            page_href = artwork[1]
            try:
                txt_ref = get_download_href(page_href)
                print(txt_ref)
                artwork_data["link"] = txt_ref
                # all_data.append((" ".join(author[0]), )) # (Author, )
            except:
                print("No txt file... :(")
            author_data["artworks"].append(artwork_data)
            recursive_counter += 1
        all_data.append(author_data)
        # print("all data: ", all_data)
    return all_data


def make_good_data(max_recursive_counter = None):
    this_Vova = Vova()

    all_data = []
    recursive_counter = 0
    autor_resave_counter = 0
    author_data = load_json_from_file("Authors.json")

    for author in author_data:
        print("Author: ", " ".join(author["name"]), " : ")

        '''
        literature =  None
        while literature is None:
            try:
                literature = get_author_books(author["link"])
            except:
                this_Vova.multi_alert()
                time.sleep(5)
        '''
        literature = this_Vova.try_loading(get_author_books, author["link"])
        # print(" ,".join(literature)[0], "\n", " ,".join(literature)[1])
        if len(literature) < min_acceptable_artwork_number:
            print("Untalented author... :(\n")
            continue
        print(literature)
        author_name = " ".join(author["name"])
        author_data = {"name": author_name, "page": author["link"], "artworks" : []}

        no_txt_counter = 0
        yes_txt_counter = 0
        for artwork in literature:
            if max_recursive_counter is not None and recursive_counter >= max_recursive_counter:
                return all_data
            if no_txt_counter > no_txt_limit and yes_txt_counter / no_txt_counter < 0.3:
                print(author_name + " - типичный КОЗЁЛ С АВТОРСКИМ ПРАВОМ!!!")
                break
            artwork_data = {"name" : artwork[0], "link" : None}
            page_href = artwork[1]
            try:
                txt_ref = get_download_href(page_href)
                print(txt_ref)
                artwork_data["link"] = txt_ref
                yes_txt_counter += 1
                # all_data.append((" ".join(author[0]), )) # (Author, )
            except:
                no_txt_counter += 1
                print("No txt file... :(")
            author_data["artworks"].append(artwork_data)
            recursive_counter += 1
        print("\n\n")
        if no_txt_counter > no_txt_limit:
            continue
        all_data.append(author_data)
        print(author_data)
        print(autor_resave_counter)
        autor_resave_counter += 1
        if autor_resave_counter > autor_resave_limit:
            autor_resave_counter = 0
            resave_good(all_data, recursive_counter)
    return all_data

def make_best_data(max_recursive_counter = None):
    wikipedia.set_lang("ru")
    this_Vova = Vova()

    all_data = []
    recursive_counter = 0
    author_resave_counter = 0
    author_data = load_json_from_file("Authors.json")

    for author in author_data:
        print("Author: ", " ".join(author["name"]), " : ")

        literature = this_Vova.try_loading(get_author_books, author["link"])
        # print(" ,".join(literature)[0], "\n", " ,".join(literature)[1])
        if len(literature) < min_acceptable_artwork_number_for_good_authors:
            print("Untalented author... :(\n")
            continue

        wiki_data = this_Vova.try_loading(rater.author_wiki, " ".join(author["name"]))
        if not wiki_data:
            print("Not the best author...\n")
            continue

        print(literature)
        author_name = " ".join(author["name"])
        author_data = {"name": author_name, "page": author["link"], "wiki" : wiki_data, "artworks" : []}

        no_txt_counter = 0
        yes_txt_counter = 0
        for artwork in literature:
            if max_recursive_counter is not None and recursive_counter >= max_recursive_counter:
                return all_data
            if no_txt_counter > no_txt_limit and yes_txt_counter / no_txt_counter < 0.3:
                print(author_name + " - типичный КОЗЁЛ С АВТОРСКИМ ПРАВОМ!!!")
                break
            artwork_data = {"name" : artwork[0], "link" : None}
            page_href = artwork[1]
            try:
                txt_ref = get_download_href(page_href)
                print(txt_ref)
                artwork_data["link"] = txt_ref
                yes_txt_counter += 1
                # all_data.append((" ".join(author[0]), )) # (Author, )
            except:
                no_txt_counter += 1
                print("No txt file... :(")
            author_data["artworks"].append(artwork_data)
            recursive_counter += 1
        print("\n\n")
        if no_txt_counter > no_txt_limit:
            continue
        all_data.append(author_data)
        print_as_json(author_data)
        print("Resave counter:", author_resave_counter)
        author_resave_counter += 1
        if author_resave_counter > autor_resave_limit:
            author_resave_counter = 0
            resave_best(all_data, recursive_counter)
    return all_data


def get_best_tmp():
    temps = os.listdir("res/")
    best_temps = []
    for temp in temps:
        if temp.startswith("Best_authors_temp_") and has_extension(temp, ".json"):
            best_temps.append(temp)

    max_number = -1
    THE_best_temp = None
    for best_temp in best_temps:
        number = int(best_temp[len("Best_authors_temp_") : best_temp.find(".")])
        if max_number < number:
            THE_best_temp = best_temp
            max_number = number
    return "res/" + THE_best_temp


def continue_making_best_data(max_recursive_counter = None):
    # TODO : CONTINUE making!

    wikipedia.set_lang("ru")
    this_Vova = Vova()

    all_data = []
    recursive_counter = 0
    author_resave_counter = 0
    author_data = load_json_from_file("Authors.json")

    for author in author_data:
        print("Author: ", " ".join(author["name"]), " : ")

        literature = this_Vova.try_loading(get_author_books, author["link"])
        # print(" ,".join(literature)[0], "\n", " ,".join(literature)[1])
        if len(literature) < min_acceptable_artwork_number_for_good_authors:
            print("Untalented author... :(\n")
            continue

        wiki_data = this_Vova.try_loading(rater.author_wiki, " ".join(author["name"]))

        if not wiki_data:
            print("Not the best author...\n")
            continue

        print(literature)
        author_name = " ".join(author["name"])
        author_data = {"name": author_name, "page": author["link"], "wiki" : wiki_data, "artworks" : []}

        no_txt_counter = 0
        yes_txt_counter = 0
        for artwork in literature:
            if max_recursive_counter is not None and recursive_counter >= max_recursive_counter:
                return all_data
            if no_txt_counter > no_txt_limit and yes_txt_counter / no_txt_counter < 0.3:
                print(author_name + " - типичный КОЗЁЛ С АВТОРСКИМ ПРАВОМ!!!")
                break
            artwork_data = {"name" : artwork[0], "link" : None}
            page_href = artwork[1]
            try:
                txt_ref = get_download_href(page_href)
                print(txt_ref)
                artwork_data["link"] = txt_ref
                yes_txt_counter += 1
                # all_data.append((" ".join(author[0]), )) # (Author, )
            except:
                no_txt_counter += 1
                print("No txt file... :(")
            author_data["artworks"].append(artwork_data)
            recursive_counter += 1
        print("\n\n")
        if no_txt_counter > no_txt_limit:
            continue
        all_data.append(author_data)
        mylang.print_dict(author_data)
        print("Resave counter:", author_resave_counter)
        author_resave_counter += 1
        if author_resave_counter > autor_resave_limit:
            author_resave_counter = 0
            resave_best(all_data, recursive_counter)
    return all_data

def make_all_good_data():
    all_data = make_good_data(None)
    all_str = json.dumps(all_data, ensure_ascii=False, indent=4)
    print(all_str)
    file = open("Good_authors.json", "w", encoding="utf-8")
    file.write(all_str)
    file.close()

def load_best_authors():
    all_data = make_best_data(None)
    all_str = json.dumps(all_data, ensure_ascii=False, indent=4)
    print(all_str)
    file = open("Best_authors.json", "w", encoding="utf-8")
    file.write(all_str)
    file.close()

def resave_best(data, num):
    all_str = json.dumps(data, ensure_ascii=False, indent=4)
    print("Resaving Best!")
    file = open("res/Best_authors_temp_" + str(num) + ".json", "w", encoding = "utf-8")
    file.write(all_str)
    file.close()

def resave_good(data, num):
    all_str = json.dumps(data, ensure_ascii=False, indent=4)
    print("Resaving!")
    file = open("res/Good_authors_temp_" + str(num) + ".json", "w", encoding = "utf-8")
    file.write(all_str)
    file.close()

def all_to_file(filename : str, recursion_limit = None):
    all_data = make_all_data(recursion_limit)
    all_str = json.dumps(all_data, ensure_ascii=False, indent=4)
    print(all_str)
    file = open(filename, "w")
    file.write(all_str)
    file.close()


def load_authors():
    lst = []
    author_data = get_author_names_and_links()
    for author in author_data:
        lst.append({ "name" : author[0], "link" : author[1] })
    string = json.dumps(lst, ensure_ascii=False, indent=4)
    print(string)
    file = open("Authors.json", "w", encoding="utf8")
    file.write(string)
    file.close()


def load_latest_best_temp():
    return load_json_from_file(get_best_tmp())

def load_best_authors_files():
    best_authors = load_latest_best_temp()
    urls = []
    dirs = []
    base_path = "D:\Projects\Literature_analyzer\\res\Books\Loading"
    for author in best_authors:
        for artwork in author["artworks"]:
            if artwork["link"] is not None:
                urls.append(artwork["link"])
                this_path = base_path + "\\" + author["name"] + "\\" + artwork["name"]
                dirs.append(make_good_filename(this_path))

    # thread_loader.multiprocess_load(urls, thread_loader.Artwork_loader, dirs)
    artwork_page = soup_cooker.cook_soup(requests.get(
        "https://royallib.com/book/betaki_vasiliy/ten_vremeni_chetirnadtsataya_kniga_stihov_20092010_godi.html").text)
    print_as_json(get_artwork_data(artwork_page))

def get_all_author_links():
    author_names = get_author_names_and_links()
    print(author_names)
    all_to_file("Test.json", recurson_limit=None)
    # print(load_authors_from_file("Authors.json"))
    print(get_artwork_data(bs(requests.get(
        "https://royallib.com/book/palama_svyatitel_grigoriy/svt_grigoriy_palama_sto_pyatdesyat_glav.html").text,
                              "html.parser")))
    load_best_authors()


if __name__ == "__main__":
    print("Don`t use the file this way!")



