import math

from rating import wikipedia_worker, yandex
import wikipedia
from lib import mylang

good_sites = {"ilibrary.ru" : 10, "litres.ru" : 10, "libfox.ru" : 7, "онлайн-читать.рф" : -1,
              "bookscafe.net" : 7, "classica-online.ru" : 4, "librebook.me" : 6, "litmir.me" : 4, "all-the-books.ru" : 4}
good_site_edge = 10





def rate_author_search_result(author : str, result : str) -> bool:  # If result matches to author name ( all words from name are here )
    author_traits = author.split()
    if len(author_traits) < 2:
        return False
    # Trying to find 2 or more in united title and block ( i
    counter = 0
    edge = 2 if counter <= 4 else int(len(author_traits) / 1.8)
    for author_part in author_traits:
        if result.find(author_part) != -1:
            counter += 1
    print(author, result, counter)
    return counter >= edge


def matches_author_wiki(author_list : list, result : str) -> bool:
    if len (author_list) == 1:
        return False
    # Finding initials
    all_init_words = result.split(" ")
    text_initials = []
    author_initials = []
    inits_done = [0 for _ in range(len(author_list))]
    initial_weight = 0

    for author_particle in author_list:
        if len(author_particle) == 2 and author_particle[1] == '.' and author_particle[0].isupper():
            author_initials.append(author_particle)

    for poss_init in all_init_words:
        if len(poss_init) == 2 and poss_init[1] == '.' and poss_init[0].isupper(): # This word in text is an initial
            text_initials.append(poss_init)
            if poss_init in author_list:
                inits_done[author_list.index(poss_init)] += 0.5
        if len(poss_init) >= 1 and poss_init[0].isupper() and poss_init[0] + '.' in author_initials:
            inits_done[author_list.index(poss_init[0] + '.')] += 2
    real_words = mylang.split_words(result)
    for word in real_words:
        if word in author_list:
            inits_done[author_list.index(word)] += 3

    count_good_inits = 0
    for author_particle in inits_done:
        if author_particle >= 1:
            count_good_inits += 1
            count_good_inits += min((author_particle - 1) / 3, (5 - 1) / 3)
        else:
            count_good_inits -= (1 - author_particle) * 1.5

    initial_edge = 2 if len(author_list) == 3 else len(author_list)
    if len(author_list) == 2:
        initial_edge = 1.7
    # 1 :   :(
    # 2 :   word and initial => 3
    # 3 :   word and initial => 3
    # 4 :   word and two initials => 4
    # 5 :   2 words and initial => 5

    authoric_words = {
          "автор" : 100, "писатель" : 100, "поэт" : 100, "литератор" : 50, "критик" : 50,
          "литература" : 60, "драматург" : 70, "сценарист" : 50, "деятель искусств" : 50,
          "комиксист" : 50, "произведений" : 100, "произведение" : 100, "книга" : 100,
          "комикс" : 60, "комиксы" : 60, "комиксов" : 60, "книги" : 100, "книгу" : 100,
          "прозаик" : 80, "писателей" : 100, "мыслителей" : 60, "тираж" : 70, "произведения" : 100,
          "драма" : 100, "трилогия" : 100, "роман" : 100, "романы" : 100, "романов" : 100, "автобиографические" : 100, "цикл" : 30, "очерков" : 100,
          "литературе" : 100, "литературой" : 70, "печатался" : 100, "печататься" : 100, "спектакль" : 40, "пьеса" : 80, "жанр" : 100, "сценарий" : 30, "пьесы" : 80,
          "фантаст" : 100, "фантастика" : 100, "читатель" : 30, "книгой" : 100, "книг" : 100, "книгами" : 100, "научно" : 20, "художественных" : 100, "жанрах" : 100,
    }

    this_authoric_words = []

    authority_counter = 0
    for word in real_words:
        if word.lower() in authoric_words:
            this_authoric_words.append(word)
            authority_counter += authoric_words[word.lower()]

    if this_authoric_words:
        pass
        # print("Authoric words: ", end = "")
        # print(", ".join(this_authoric_words))

    all_edge = initial_edge + 2

    total = 0
    authority_edge_0 = 120
    authority_edge_1 = 300 # More: ...
    authority_edge_2 = 1000 # More: ... ... ...

    minimal_goods = max(len(author_list), 3)

    if authority_counter > authority_edge_0:
        total += len(author_list)
        if authority_counter > authority_edge_1:
            meaning_authority = min(authority_counter, authority_edge_2)
            total += len(author_list) * math.sqrt(meaning_authority - authority_edge_1) / 20

    total_authority_result = total

    total += count_good_inits

    total_edge = 0

    # print("Authority result: ", total_authority_result, "Goods: ", count_good_inits, "Total =", total)

    return authority_counter >= authority_edge_0 and count_good_inits > minimal_goods and total > total_edge

def rate_author(name : str) -> bool:
    search_res = yandex.search_first(name + " писатель", amount = 3, site="wikipedia.org")
    for this_res in search_res:
        if rate_author_search_result(name, this_res):
            return True
    return False


def is_from_sites(site):
    for pos_site in good_sites:
        if yandex.is_from_site(site, pos_site):
            return True
    return False


def get_good_site(link : str) -> str:
    for pos_site in good_sites:
        if link.find(pos_site):
            return pos_site
    raise Exception("It should be good site!")


def rate_text(author : str, book : str) -> (bool, int):
    search_res = yandex.search_data(author + " " + book + " книга")
    rating = 0

    good_site_content = []

    for this_res in search_res:
        if is_from_sites(this_res[1]):
            good_site_content.append(this_res[0] + " \n" + this_res[2])


    for good_content in good_site_content:
        name = good_content[0]
        link = good_content[1]
        data = good_content[2]
        # if matches_book_search_result(author, book, good_content):
        #    rating += good_sites[get_good_site(link)]

        # TODO : matching : when???
    return rating > good_site_edge, rating


def author_wiki(name : str) -> dict:
    res = {}
    search_result = wikipedia_worker.wiki_search(name)
    # print(search_result)
    if not search_result["status"]:
        return {}

    page = wikipedia.page(search_result["title"])
    title = page.title
    summary = page.summary
    html = page.html()
    quick_table = wikipedia_worker.get_quick_table(html)

    if not matches_author_wiki(name.split(" "), title + "  " + summary):
        return {}

    authoric_words = wikipedia_worker.get_authoric_words(title + "  " + summary)
    authority = wikipedia_worker.get_authority(description=summary, author_list=name.split(" "))
    lifetime = mylang.clever_life(page, quick_table)
    res["life"] = lifetime

    res["raw_title"] = search_result["title"]
    res["title"] = mylang.del_nonletters(search_result["title"])

    res["authority"] = authority
    res["authoric_words"] = authoric_words
    res["additional_properties"] = quick_table
    # TODO: improve

    res["load"] = True

    return res


def wiki_rate_author(name : str) -> bool:
    search_result = wikipedia_worker.wiki_search(name)
    if not search_result["status"]:
        return False

    page = wikipedia.page(search_result["title"])
    print(page.categories)
    print(page.summary)
    print(page.content)


if __name__ == "__main__":
    '''
    authors = royal_parser.load_authors_from_file("Authors.json")
    wikipedia.set_lang("ru")
    result = []

    for author in authors:
        name = author["name"]
        print("Searching author:", " ".join(name))
        this_data = author_wiki(" ".join(name))
        if "success" in this_data and this_data["success"]:
            result.append( {"name" : name, "data" : this_data} )
            print(json.dumps(this_data, ensure_ascii=False, indent=4))

    all_str = json.dumps(result, ensure_ascii=False, indent=4)
    print("Saving!")
    file = open("Good_authors_test.json", "w", encoding="utf-8")
    file.write(all_str)
    file.close()
    '''


    authors = ["Абнетт Дэн", "Пётр Ильич", "Айзек Азимов", "Пушкин Александр", "Толстой Лев", "Владимир Латыпов", "Ситников Андрей", "Георгий Шульга",
                "Аъзек Азимов", "Абнетт Дэн", "Азарьев Олег", ""
               "Вася Пупкин", "Геворг Макорян", "Владимир Путин"]

    wikipedia.set_lang("ru")
    for author in authors:
        print("Trying to find:", author, end = ": \n")
        mylang.print_json(author_wiki(author))

        print("\n\n")
        '''
        search_res = wikipedia_worker.wiki_search(author)
        if not search_res["status"]:
            print("Can`t find...")
            continue
        wiki_page = wikipedia.page(search_res["title"])
        print("Life:", mylang.clever_life(wiki_page), "Result:", author_wiki(author))
        '''