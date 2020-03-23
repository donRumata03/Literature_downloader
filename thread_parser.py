from mylang import *
from threading import Thread
import royal_parser
import requests
from soup_cooker import *

all_tasks_performed = 0
all_tasks_to_do = 0

author_data = []
number_of_threads = 10
start = datetime.now()

errors_to_print = []

class Multithread_parser(Thread):
    tasks : list = []
    workers = []
    this_Vova = None
    result = None
    target_file = None

    def __init__(self, tasks : list, parser : Type):
        Thread.__init__(self)
        self.this_Vova = Vova()
        self.tasks = tasks
        self.workers = [parser(tasks[i], self.this_Vova) for i in range(len(tasks))]
        self.result = [-1 for _ in range(len(tasks))]
        self.target_file = "res/thread_parse_results/from " + " ".join(self.tasks[0]["name"]) + " to " + " ".join(self.tasks[-1]["name"]) + ".json"
    def run(self):
        global all_tasks_performed
        for i, worker in enumerate(self.workers):
            self.result[i] = {"name" : self.tasks[i]["name"], "link" : self.tasks[i]["link"],
                            "artworks" : worker.do_work()}
            all_tasks_performed += 1
            cur_percent = all_tasks_performed / len(author_data) * 100
            percent_left = 100 - cur_percent
            if random.random() < 0.01:
                now = datetime.now()
                this_time = (now - start).total_seconds()
                speed = cur_percent / this_time # percents per second
                print("Time now: " + str(this_time) + "; Tasks performed:", all_tasks_performed, "of", str(len(author_data)) + ";", str(cur_percent) + "% (Speed : " + str(speed) + " pps); Time left:",
                      percent_left / speed / 60, "minutes")
        save_as_json(self.result, self.target_file)


class Multithread_art_parser(Thread):
    tasks : list = []
    workers = []
    this_Vova = None
    result = None
    target_file = None

    def __init__(self, tasks: list, parser: Type):
        Thread.__init__(self)
        self.this_Vova = Vova()
        self.tasks = tasks
        self.workers = [parser(tasks[i], self.this_Vova) for i in range(len(tasks))]
        self.result = []

        if not self.tasks:
            return

        self.target_file = "res/thread_art_parse_results/from " + " ".join(self.tasks[0]["name"]) + " to " + " ".join(
            self.tasks[-1]["name"]) + ".json"
        print("This Thread target path:", self.target_file)


    def run(self):
        if not self.tasks:
            return
        global all_tasks_performed
        for i, worker in enumerate(self.workers):
            this_res = worker.do_work()
            all_tasks_performed += 1
            if this_res is None:
                continue

            self.result.append(this_res)

            # Process Info
            percent = 100 * all_tasks_performed / all_tasks_to_do
            percent_left = 100 - percent
            if random.random() < 0.1:
                now = datetime.now()
                this_time = (now - start).total_seconds()
                speed = percent / this_time  # percents per second
                print("Time now: " + str(this_time) + "; Tasks performed:", all_tasks_performed, "of",
                      str(all_tasks_to_do) + ";", str(percent) + "% (Speed : " + str(speed * 60) + " ppm); Time left:",
                      percent_left / speed / 60, "minutes")
        save_as_json(self.result, self.target_file)


class Parser:
    task = None
    this_Vova = None
    def __init__(self, task, this_vova):
        self.task = task
        self.this_Vova = this_vova

    def do_work(self):
        literature = self.this_Vova.lazy_try_loading(royal_parser.get_author_books, 3, self.task["link"])
        if literature is None:
            print('\033[91m')
            print("Can`t load this author`s artworks:", self.task["name"])
            print('\033[0m')
            return None
        return literature

    def __str__(self):
        return str(self.task)

class Art_parser:
    """
    Processes one author
    """
    author_artworks : List[dict]
    this_Vova : Vova
    old_author_data : dict
    def __init__(self, author_info : dict, vova):
        self.author_artworks = author_info["artworks"]
        self.this_Vova = vova
        self.old_author_data = author_info

    def do_partial_work(self, index) -> Optional[dict]:
        global errors_to_print
        response = self.this_Vova.lazy_try_loading(requests.get, 2, self.author_artworks[index]["link"])
        if response is None:
            msg = "Error occurred while downloading this artwork:" + self.author_artworks[index]["name"] + \
                      "written by author: " + " ".join(self.old_author_data["name"])
            print_red(msg)
            errors_to_print.append(msg)
            return None
        page = cook_soup(response.text)
        result = royal_parser.get_artwork_data(page)
        return result

    def do_work(self):
        for index in range(len(self.author_artworks)):
            # res.append(self.do_partial_work(index))
            this_res = self.do_partial_work(index)
            self.old_author_data["artworks"][index]["page_data"] = this_res
        return self.old_author_data


def multithread_parse(tasks : list, threads_number : int, worker_type : Type, thread_type : Type):
    # task_sets = []
    task_sets = [[] for _ in range(threads_number)]
    cursor = 0
    tasks_per_thread = int(len(tasks) / threads_number)

    container_id = 0
    for task_id, task in enumerate(tasks):
        task_sets[container_id].append(task)
        container_id += 1
        if container_id == len(task_sets):
            container_id = 0


    #
    # for thread_number in range(threads_number):
    #     last_cursor = cursor
    #     cursor += tasks_per_thread
    #     task_sets.append(tasks[last_cursor : cursor])
    #
    # if cursor != len(tasks):
    #     task_sets.append(tasks[cursor:])



    threads = []

    for task in task_sets:
        this_parser = thread_type(task, worker_type)
        threads.append(this_parser)


    print_good_info("Performed task distribution!", f"({len(threads)} Threads)")

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def multithreading_good_load():
    global author_data, start
    author_data = load_json_from_file("Authors.json")
    start = datetime.now()
    multithread_parse(author_data, number_of_threads, Parser, Multithread_parser)


def multi_parse_artworks():
    global all_tasks_to_do
    filename = "All_authors_artworks.json"
    # filename = "Test_artworks.json"
    art_data = load_json_from_file(filename)
    print_good_info("Loaded data to process!")
    all_tasks_to_do = len(art_data)
    print_good_info("All tasks to do:", all_tasks_to_do, "(Authors)")
    multithread_parse(art_data, number_of_threads, Art_parser, Multithread_art_parser)

    for i in range(10):
        print("\n")
    print_props("Here are some errors occurred during downloading:\n\n", console_color.BOLD, console_color.YELLOW)

    for msg in errors_to_print:
        print_red(msg)

    print_good_info("Process successfully finished!")


if __name__ == "__main__":
    multi_parse_artworks()



strange_program = """
def make_best_data(max_recursive_counter = None):
    wikipedia.set_lang("ru")
    this_Vova = Vova()

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
"""
