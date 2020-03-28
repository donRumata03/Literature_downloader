from royal_parsing.author_page_scraper import *
import lib.soup_cooker as soup_cooker
import requests

artwork_error_counter = 0

class artwork_page_parser(Thread):
    tasks : list
    id : int
    def __init__(self, _tasks, _id):
        Thread.__init__(self)
        self.tasks = _tasks
        self.id = _id
        self.target_path = f"D:\\Projects\\Literature_downloading\\res\\artwork_pages_temp\\thread_{self.id}_result.json"

    def run(self):
        global artwork_error_counter
        res = []
        for task in self.tasks:
            try:
                this_res = scrape_author_artworks_pages(task)
                res.append(this_res)
            except Exception as e:
                print_exception(e)
                artwork_error_counter += 1
                print("Error here:", task)

            loading_controller.update()
        to_utf8_json_file(res, self.target_path)


def get_artwork_data(artwork_content : bs) -> Optional[dict]: # {name, genre, link... }
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
        return None

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
    res["download_link"] = download_href
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

def scrape_artwork_page(link) -> dict:
    artwork_content = requests.get(link)
    return get_artwork_data(bs(artwork_content.text, "html.parser"))

def scrape_author_artworks_pages(author_data : dict):
    author_name = author_data["name"]
    author_link = author_data["link"]
    author_artworks = author_data["artworks"]

    new_author_artworks = []

    for artwork_data in author_artworks:
        artwork_link = artwork_data["link"]
        new_author_artworks.append(
            {
                "name" : artwork_data["name"],
                "page_link" : artwork_link,
                "page_data" : scrape_artwork_page(artwork_link)
            }
        )

    return \
        {
            "name" : author_name,
            "link" : author_link,
            "artworks" : new_author_artworks
        }


def launch_artwork_page_parsing(debug = False):
    threads = 200

    author_data = load_author_artworks_from_file() if not debug else from_utf8_json_file("D:\\Projects\\Literature_downloading\\res\\tests\\Test_artworks.json")
    # Generate tasks:

    tasks = author_data
    print_good_info(f"All tasks to solve: {len(tasks)}, threads: {threads}")
    # Distribute tasks:
    task_sets = distribute_tasks(tasks, threads)

    # Launch
    loading_controller.init(len(tasks), 0.05, 70)

    thread_solve(task_sets, artwork_page_parser)

    print_good_info("All tasks solved!")
    print_red("Errors occurred:", error_counter, f"of all {len(tasks)} tasks!")


def make_p_patch():
    pass


if __name__ == '__main__':
    # print_as_json(scrape_artwork_page("https://royallib.com/book/babchenko_arkadiy/voyna_i_mir_po_prinugdeniyu.html"))
    launch_artwork_page_parsing()
