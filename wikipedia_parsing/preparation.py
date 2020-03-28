import os

from royal_parsing.author_page_scraper import load_author_artworks_from_file
from lib.mylang import print_as_json, to_utf8_json_file, from_utf8_json_file

ARTWORK_CUTTING_LIMIT = 2

def cook_data(artwork_cutting_limit : int):
    all_data = load_author_artworks_from_file()

    res = []
    for author in all_data:
        if "" in author["name"].split(" "):
            print(author)
        if len(author["artworks"]) >= artwork_cutting_limit:
            res.append(
                author
            )
    return res


def load_filtered_data():
    base_path = "D:\\Projects\\Literature_downloading\\wikipedia_parsing"
    last_node = f"filtered_authors(eq_or_more_than_{ARTWORK_CUTTING_LIMIT}_artworks).json"
    res_path = os.path.join(base_path, last_node)
    if os.path.exists(res_path):
        pass
    else:
        print("Cooking data again!")
        to_utf8_json_file(cook_data(ARTWORK_CUTTING_LIMIT), res_path)
    return from_utf8_json_file(res_path)


if __name__ == '__main__':
    # to_utf8_json_file(cook_data(ARTWORK_CUTTING_LIMIT), f"filtered_authors(eq_or_more_than_{ARTWORK_CUTTING_LIMIT}_artworks).json")
    print_as_json(len(load_filtered_data()))