from wikipedia_parsing.preparation import load_filtered_data

from lib.mylang import *
from rating.wikipedia_worker import *
from rating.rater import *
from threading_downloading.thread_pool import *

from wikipedia_parsing.collect_wiki_res import *

wiki_errors = 0

number_of_temp_savings = 200

class thread_wiki_parser(Thread):
    tasks: list
    id: int

    def __init__(self, _tasks, _id):
        Thread.__init__(self)
        self.tasks = _tasks
        self.id = _id
        self.target_path = f"D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\thread_{self.id}_result.json"
        self.temp_dir = f"D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\thread_{self.id}_temp"
        try:
            os.mkdir(self.temp_dir)
        except:
            pass
        self.temp_file_number = 0

    def get_temp_filename(self):
        return os.path.join(self.temp_dir, str(self.temp_file_number) + ".json")

    def run(self):
        global wiki_errors
        res = []
        processed_authors = []
        this_Vova = Vova()
        saving_counter = 0
        saving_part = 1 / number_of_temp_savings
        max_saving_counter = saving_part * len(self.tasks)

        self.temp_file_number = 0
        for task in self.tasks:
            name = task["name"]

            try:
                got_data = author_wiki(name)
                if got_data["is_famous"]:
                    this_res = \
                        {
                            "name": name,
                            "artworks": task["artworks"],
                            "wiki_data" : got_data
                        }
                    res.append(this_res)
                processed_authors.append(task)
                    # print(this_res)


            # TODO: Special handling deny wiki exceptions!

            except Exception as e:
                print_exception(e)
                wiki_errors += 1
                print_red("Error here:", name)

            loading_controller.update()
            saving_counter += 1

            if saving_counter > max_saving_counter:
                self.temp_file_number += 1
                saving_counter = 0
                to_utf8_json_file(
                    {
                        "res": res,
                        "processed" : processed_authors
                    },
                    self.get_temp_filename())
                print(f"Saved new temp file: {self.temp_file_number}")

        to_utf8_json_file(res, self.target_path)

def get_temp_data(res_save_path : str = "D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\last_res.json",
                  processed_save_path : str = "D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\last_processed.json"):
    temp_folders = full_lsdir("D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp")

    temp_res = []
    temp_checked = []
    for folder in temp_folders:
        if "." in folder:
            continue
        # Get last temp:
        file_names = sorted([i.split(".")[-2] for i in os.listdir(folder)])
        if not file_names:
            continue
        best_filename = file_names[-1]
        full_best_filename = os.path.join(folder, str(best_filename) + ".json")
        file_data = from_utf8_json_file(full_best_filename)
        temp_res.extend(file_data["res"])
        temp_checked.extend(file_data["processed_authors"])
        """
        for file in full_lsdir(folder):

            file_data = from_utf8_json_file(file)

            this_res = file_data["res"]
            this_checked = file_data["processed_authors"]

            all_res.extend(this_res)
            all_checked.extend(this_checked)
        """
    # to_utf8_json_file(all_res, res_save_path)


    # Res processing:
    from_all_res_file = []
    if os.path.exists(res_save_path):
        from_all_res_file = from_utf8_json_file(res_save_path)

    names_had = set([i["name"] for i in from_all_res_file])

    res_appended_counter = 0
    all_res = from_all_res_file[:]
    for temp_author in temp_res:
        if temp_author["name"] in names_had:
            pass
        else:
            res_appended_counter += 1
            all_res.append(temp_author)

    to_utf8_json_file(all_res, res_save_path)

    # Processed processing

    from_all_processed_file = []
    if os.path.exists(processed_save_path):
        from_all_processed_file = from_utf8_json_file(processed_save_path)

    names_had = set([i["name"] for i in from_all_processed_file])

    all_processed = from_all_processed_file[:]
    processes_append_counter = 0
    for temp_author in temp_checked:
        if temp_author["name"] in names_had:
            pass
        else:
            processes_append_counter += 1
            all_processed.append(temp_author)

    # to_utf8_json_file(all_processed, processed_save_path)

    print_good_info(f"Res appended: {res_appended_counter}, Processed appended: {processes_append_counter}")

    return all_res, all_processed


def get_not_loaded_authors():
    all_authors = load_filtered_data()

    _pre_res, _pre_checked = get_temp_data()
    _pre_names = set([author["name"] for author in _pre_checked])

    not_loaded_authors = []
    loaded_authors = []
    for author in all_authors:
        if author["name"] not in _pre_names:
            not_loaded_authors.append(author)
            # print(author)
        else:
            loaded_authors.append(author)

    print_good_info(f"Not loaded authors: {len(not_loaded_authors)}")


    return not_loaded_authors


def launch_wiki_parse():
    threads = 7

    test_rating = "D:\\Projects\\Literature_downloading\\res\\tests\\wiki_test.json"
    # authors_to_rate = load_filtered_data()
    authors_to_rate = get_not_loaded_authors()

    temp_folders_to_delete = [os.path.join("D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp", f) for f in os.listdir(
        "D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp")
                              if "_temp" in f]

    for tf in temp_folders_to_delete:
        pass
        # os.remove(tf)


    # authors_to_rate = from_utf8_json_file(test_rating)
    wikipedia.set_lang("ru")

    print_good_info("All tasks:", len(authors_to_rate))

    task_sets = distribute_tasks(authors_to_rate, threads)

    loading_controller.init(len(authors_to_rate), 0.1, 100)
    thread_solve(task_sets, thread_wiki_parser)


if __name__ == '__main__':
    launch_counter = 0
    while True:
        print_good_info(f"Launching step: {launch_counter}")
        # cong_wiki_res()

        launch_wiki_parse()
        launch_counter += 1
