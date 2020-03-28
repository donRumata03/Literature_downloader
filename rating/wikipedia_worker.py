import math

from bs4 import BeautifulSoup as bs
import wikipedia
from lib import mylang, soup_cooker
from lib.mylang import print_red
from lib.mylang import *

authoric_words = {
        "автор": 100, "писатель": 100, "поэт": 100, "литератор": 50, "критик": 50,
        "литература": 60, "драматург": 70, "сценарист": 50, "деятель искусств": 50,
        "комиксист": 50, "произведений": 100, "произведение": 100, "книга": 100,
        "комикс": 60, "комиксы": 60, "комиксов": 60, "книги": 100, "книгу": 100,
        "прозаик": 80, "писателей": 100, "мыслителей": 60, "тираж": 70, "произведения": 100,
        "драма": 100, "трилогия": 100, "роман": 100, "романы": 100, "романов": 100, "автобиографические": 100,
        "цикл": 30, "очерков": 100,
        "литературе": 100, "литературой": 70, "печатался": 100, "печататься": 100, "спектакль": 40, "пьеса": 80,
        "жанр": 100, "сценарий": 30, "пьесы": 80,
        "фантаст": 100, "фантастика": 100, "читатель": 30, "книгой": 100, "книг": 100, "книгами": 100, "научно": 20,
        "художественных": 100, "жанрах": 100,
    }


def get_quick_table(page : str):
    res = {}
    full_data = bs(page, "html.parser")
    quick_data = bs(str(full_data.find('table', class_ = "infobox")), "html.parser")
    
    for child in quick_data.recursiveChildGenerator():
        if soup_cooker.has_tag(child, "<tr>") and str(child).find("<td") != -1 and str(child).find("<th") != -1 and not child.find_all('a', class_="image"):
            key = child.find('th').text.strip().replace("\xa0", " ")
            value = child.find('td').text.strip()
            res[key] = value

    return res


def get_authoric_words(string : str) -> list:
    real_words = mylang.split_words(string)
    this_authoric_words = []

    authority_counter = 0
    for word in real_words:
        if word.lower() in authoric_words:
            this_authoric_words.append(word)

    return this_authoric_words


def get_authority(description : str, author_list : list) -> int:
    real_words = mylang.split_words(description)

    this_authoric_words = []

    authority_counter = 0
    for word in real_words:
        if word.lower() in authoric_words:
            this_authoric_words.append(word)
            authority_counter += authoric_words[word.lower()]

    total = 0
    authority_edge_0 = 120
    authority_edge_1 = 300  # More: ...
    authority_edge_2 = 1000  # More: ... ... ...


    if authority_counter > authority_edge_0:
        total += len(author_list)
        if authority_counter > authority_edge_1:
            meaning_authority = min(authority_counter, authority_edge_2)
            total += len(author_list) * math.sqrt(meaning_authority - authority_edge_1) / 20

    total_authority_result = total
    return total_authority_result

def wiki_search(subject):
    search_result = wikipedia.search(subject)
    if not search_result:
        suggest = wikipedia.suggest(subject)
        if suggest:
            search_result = suggest[0]
        else:
            return { "status" : False }
    else:
        search_result = search_result[0]
    try:
        response = wikipedia.page(search_result)
    except wikipedia.exceptions.DisambiguationError as e:
        # print_red(e.options)
        return { "status" : False }
    except:
        print_red("Some wiki error...")
        return { "status" : False }

    return {"status" : True, "title": response.title, "url": response.url}

def clever_life(response : wikipedia.WikipediaPage, quick_table = None):
    res = {}

    if quick_table is None:
        quick_table = get_quick_table(response.html())
    birthday = -1
    death_day = -1
    age = -1; alive = True; precision = True

    birthday_words = {"Дата рождения", "Рождение", "Родился", "Родилась", "Рождён"}
    death_words = {"Дата смерти", "Смерть", "Умер", "Умерла", "Убит"}

    if "Дата рождения" in quick_table:
        raw_birthday = find_4_digit_nums(quick_table["Дата рождения"])
        if raw_birthday:
            birthday = raw_birthday[0]
        if raw_birthday and "Дата смерти" in quick_table:
            death_day = find_4_digit_nums(quick_table["Дата смерти"])[0]
            alive = False
            age = death_day - birthday
        elif raw_birthday:
            alive = True
            age = 2020 - birthday


    if birthday == -1:
        precision = False
        summary = response.summary
        bad_data = get_life_time(summary)
        if "born" in bad_data:
            birthday = bad_data["born"]
            if "end" in bad_data:
                death_day = bad_data["end"]
                alive = False
            else:
                death_day = 2020
                alive = True
        else:
            birthday = random.randint(1900, 2020)
            death_day = random.randint(birthday, 2500)
            alive = death_day > 2020
        age = death_day - birthday
    res = {"alive" : alive, "birth_day" : birthday, "death_day" : death_day, "age" : age, "precision" : precision}
    return res


if __name__ == "__main__":
    wikipedia.set_lang("ru")
    searched = wiki_search("Лев Толстой")
    if searched["status"]:
        page = wikipedia.page(searched["title"])
        title = page.title
        summary = page.summary
        html = page.html()
        print(get_quick_table(html))