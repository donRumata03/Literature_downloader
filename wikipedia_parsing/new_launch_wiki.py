import shutil

from wikipedia_parsing.preparation import load_filtered_data
from lib.mylang import *
from rating.wikipedia_worker import *
from rating.rater import *
from threading_downloading.thread_pool import *
from wikipedia_parsing.collect_wiki_res import *

wiki_errors = 0
number_of_temp_savings = 10

tasks_performed = 0

class thread_wiki_parser(Thread):
    tasks: list
    id: int
    res : list
    processed : list

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
        self.res = []
        self.processed = []

    def get_temp_filename(self):
        return os.path.join(self.temp_dir, str(self.temp_file_number) + ".json")

    def get_data_for_temp(self):
        return {
            "res" : self.res,
            "processed" : self.processed
        }

    def save_temp(self):
        to_utf8_json_file(self.get_data_for_temp(), self.get_temp_filename())

    def run(self):
        global wiki_errors, tasks_performed
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
                    self.res.append(this_res)
                self.processed.append(task)

            except Exception as e:
                print_exception(e)
                wiki_errors += 1
                print_red(f"Error here:{name}, Errors total: {wiki_errors} of {tasks_performed} ({100 * wiki_errors / (1 + tasks_performed)} %)")

            tasks_performed += 1
            loading_controller.update()
            saving_counter += 1

            if saving_counter > max_saving_counter:
                self.temp_file_number += 1
                saving_counter = 0
                self.save_temp()
                print(f"Saved new temp file: {self.temp_file_number}")

        to_utf8_json_file(self.get_data_for_temp(), self.target_path)

def delete_temps():
    base_path = "D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp"

    to_delete = [os.path.join(base_path, f) for f in os.listdir(base_path) if "thread" in f]
    for f in to_delete:
        if "." not in f:
            shutil.rmtree(f)
        else:
            os.remove(f)

def get_last_temp_filename(directory : str) -> Optional[str]:
    if not os.listdir(directory):
        return None
    return os.path.join(directory, str(max([int(i.split(".")[-2]) for i in os.listdir(directory)])) + ".json")

def collect_data() -> None:
    """
    Moves data from temporary files to files:
    res -> D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\last_res.json
    processed -> D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\last_processed.json
    """

    print("******************************************************")
    print("*********** Collecting thread results ****************")
    print("******************************************************")

    base_path = "D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp"
    base_dir_list = os.listdir(base_path)

    json_init_string = "[\n\t\n]"

    last_res_filename = "last_res.json"
    last_processed_filename = "last_processed.json"

    last_res_path = os.path.join(base_path, last_res_filename)
    last_processed_path = os.path.join(base_path, last_processed_filename)

    if last_res_filename not in base_dir_list:
        op = open(last_res_path, "w")
        op.write(json_init_string)
        op.close()

    if last_processed_filename not in base_dir_list:
        op = open(last_processed_path, "w")
        op.write(json_init_string)
        op.close()

    last_res_data = from_utf8_json_file(last_res_path)
    last_processed_data = from_utf8_json_file(last_processed_path)

    print_props(f"Now processed: {len(last_processed_data)}", console_color.BLUE, console_color.BOLD)
    print_props(f"Now res: {len(last_res_data)}", console_color.BLUE, console_color.BOLD)

    res_names = set([author["name"] for author in last_res_data])
    processed_names = set([author["name"] for author in last_processed_data])

    total_res = last_res_data[:]
    total_processed = last_processed_data[:]

    res_from_temp_counter = 0
    processed_from_temp_counter = 0

    for temp_file_name in [get_last_temp_filename(i) for i in [os.path.join(base_path, directory) for directory in os.listdir(base_path) if "temp" in directory] if i is not None]:
        if temp_file_name is None:
            continue
        try:
            temp_data = from_utf8_json_file(temp_file_name)
        except:
            continue

        temp_res = temp_data["res"]
        temp_processed = temp_data["processed"]


        for res_author in temp_res:
            if res_author["name"] not in res_names:
                total_res.append(res_author)
                res_from_temp_counter += 1


        for processed_author in temp_processed:
            if processed_author["name"] not in processed_names:
                total_processed.append(processed_author)
                processed_from_temp_counter += 1


    res_names = set([author["name"] for author in total_res])
    processed_names = set([author["name"] for author in total_processed])

    res_from_results_counter = 0
    processed_from_results_counter = 0
    for result_file_name in [i for i in [os.path.join(base_path, directory) for directory in os.listdir(base_path) if "result" in directory] if i is not None]:
        if result_file_name is None:
            continue
        try:
            temp_data = from_utf8_json_file(result_file_name)
        except:
            continue

        temp_res = temp_data["res"]
        temp_processed = temp_data["processed"]

    
        for res_author in temp_res:
            if res_author["name"] not in res_names:
                total_res.append(res_author)
                res_from_results_counter += 1


        for processed_author in temp_processed:
            if processed_author["name"] not in processed_names:
                total_processed.append(processed_author)
                processed_from_results_counter += 1

    print_good_info(f"Appended to res from temps: {res_from_temp_counter}")
    print_good_info(f"Appended to processed from temps: {processed_from_temp_counter}")

    print_good_info(f"Appended to res from reses: {res_from_temp_counter}")
    print_good_info(f"Appended to processed from reses: {processed_from_temp_counter}")

    print_good_info(f"Total size of res: {len(total_res)}")
    print_good_info(f"Total size of processed: {len(total_processed)}")

    to_utf8_json_file(total_res, last_res_path)
    to_utf8_json_file(total_processed, last_processed_path)

    print("___________________________________________________")



def get_temp_processed() -> list:
    filename = "D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\last_processed.json"
    return from_utf8_json_file(filename)


def get_loaded_and_not_loaded_authors():
    all_authors = load_filtered_data()

    already_processed = get_temp_processed()
    processed_names = set([author["name"] for author in already_processed])

    not_loaded_authors = []
    loaded_authors = []
    for author in all_authors:
        if author["name"] in processed_names:
            loaded_authors.append(author)
        else:
            not_loaded_authors.append(author)

    print_good_info(f"Loaded authors: {len(loaded_authors)}")
    print_good_info(f"Not loaded authors: {len(not_loaded_authors)}")

    return loaded_authors, not_loaded_authors


def get_not_loaded_authors():
    return get_loaded_and_not_loaded_authors()[1]

def launch_wiki_parse():
    threads = 100

    collect_data()
    delete_temps()
    authors_to_rate = get_not_loaded_authors()

    wikipedia.set_lang("ru")

    print_good_info("All tasks:", len(authors_to_rate))

    task_sets = distribute_tasks(authors_to_rate, threads)

    loading_controller.init(len(authors_to_rate), 0.1, 100)
    thread_solve(task_sets, thread_wiki_parser)



if __name__ == '__main__':
    # delete_temps()
    # collect_data()
    # d = get_not_loaded_authors()
    # print(get_last_temp_filename("D:\\Projects\\Literature_downloading\\res\\wiki_rate_temp\\test"))

    MODE = 2
    if MODE == 2:
        for i in range(5):
            launch_wiki_parse()
    elif MODE == 1:
        launch_wiki_parse()
    else:
        print("Usage : paste MODE = 1 or 2, not", MODE)

