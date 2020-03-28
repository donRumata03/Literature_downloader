from lib.soup_cooker import *
from royal_parsing.author_letter_link_parser import *
from threading_downloading.thread_pool import *


error_counter = 0


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


def parse_author_page(name : str, link : str) -> dict:
    parse_res = get_author_books(link)
    return \
    {
        "name" : name,
        "link" : link,
        "artworks" : parse_res
    }

class author_page_parser(Thread):
    id : int
    tasks : List[list]
    def __init__(self, tasks : List[list], thread_id : int):
        Thread.__init__(self)
        self.tasks = tasks
        self.id = thread_id
        self.target_path = os.path.join("D:\\Projects\\Literature_downloading\\res\\author_pages_p_patch_temp", f"thread_{self.id}_result.json")
        print(f"Thread: {self.id} working, path: {self.target_path}")

    def run(self):
        global error_counter
        res = []
        for task in self.tasks:
            try:
                this_res = parse_author_page(task[0], task[1])
                res.append(this_res)
            except:
                error_counter += 1
                print("Error here:", task)
            loading_controller.update()
        to_utf8_json_file(res, self.target_path)


def launch_page_parsing():
    threads = 20

    # Generate tasks:
    loaded = load_author_page_links_from_file()
    tasks = [(name, loaded[name]) for name in loaded]
    # ('Гноевой Роман', 'https://royallib.com/author/gnoevoy_roman.html'),
    # Spread tasks:
    task_sets = distribute_tasks(tasks, threads)
    # Launch thread working
    print_good_info("All tasks:", len(tasks), "pcs.")
    loading_controller.init(target_tasks=len(tasks), update_probability=0.05, gate_width=100)
    thread_solve(task_sets, author_page_parser)

    print_good_info("All tasks finished!")
    print_red(f"During process {error_counter} errors occurred of all {len(tasks)} files")

def P_atch_page_parsing():
    threads = 20

    # Generate tasks:
    loaded = load_author_page_links_from_file()
    tasks = [(name, loaded[name]) for name in loaded if name[0] == "П"]
    print_as_json(tasks)
    # ('Гноевой Роман', 'https://royallib.com/author/gnoevoy_roman.html'),
    # Spread tasks:
    task_sets = distribute_tasks(tasks, threads)
    # Launch thread working
    print_good_info("All tasks:", len(tasks), "pcs.")
    loading_controller.init(target_tasks=len(tasks), update_probability=0.05, gate_width=100)
    thread_solve(task_sets, author_page_parser)

    print_good_info("All tasks finished!")
    print_red(f"During process {error_counter} errors occurred of all {len(tasks)} files")


def cong_author_page_files():
    congatanate_json_files(full_lsdir("D:\\Projects\\Literature_downloading\\res\\author_pages_temp"), "D:\\Projects\\Literature_downloading\\res\\author_pages_data.json")

def cong_author_p_patch_page_files():
    all_json = make_json_from_files(full_lsdir("D:\\Projects\\Literature_downloading\\res\\author_pages_p_patch_temp"))
    all_json.extend(make_json_from_files(["D:\\Projects\\Literature_downloading\\res\\author_pages_data.json"]))

    all_json.sort(key=lambda x: x["name"])
    print(all_json)
    #                                         "D:\\Projects\\Literature_downloading\\res\\author_pages_data.json")
    to_utf8_json_file(all_json, "D:\\Projects\\Literature_downloading\\res\\author_pages_data.json")

def load_author_artworks_from_file():
    return from_utf8_json_file("D:\\Projects\\Literature_downloading\\res\\author_pages_data.json")



if __name__ == '__main__':
    cong_author_p_patch_page_files()
    # P_atch_page_parsing()
    # launch_page_parsing()
    # cong_author_page_files()
    # print_as_json(load_author_artworks_from_file())
    # print_as_json(get_author_books("https://royallib.com/author/chayko_artemiy.html"))
