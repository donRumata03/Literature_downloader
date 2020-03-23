from statistics.statistics import get_good_auth_jsn
from threading_downloading.thread_parser import *
from threading_downloading.thread_pool import *
from threading_downloading.zip_downloader import download_zip


error_counter = 0

class thread_loader(Thread):
    id : int
    tasks : List[Dict]
    temp_dir : str

    def __init__(self, task_set : List[Dict], _id : int):
        Thread.__init__(self)
        self.id = _id
        self.tasks = task_set
        self.temp_dir = "res/thread_temp/" + str(self.id)


    def run(self):
        global error_counter
        for task in self.tasks:
            path = task["path"]
            link = task["link"]
            try:
                download_zip(link, path, self.temp_dir)
            except:
                error_counter += 1
            loading_controller.update()


def generate_tasks():
    jsn = get_good_auth_jsn()
    print_good_info("Loaded all authors JSON!")

    # Make readable tasks:
    temp_tasks = [] # There are many different tasks, each of them is:   {
    #                                                                   "path" : "...",
    #                                                                   "link" = "..."
    #                                                                }

    base_path = "D:\\Literature_data\\All_books"

    for author in jsn:
        arts = author["artworks"]
        this_tasks = []

        for art in arts:
            if "page_data" not in art:
                continue
            pg = art["page_data"]
            if "link" in pg and pg["link"] is not None:
                # Make path:..
                raw_fname = os.path.join(base_path, " ".join(author["name"]),  art["name"])
                path = make_good_filename(raw_fname)
                this_tasks.append({ "link" : pg["link"], "path" : path })
        temp_tasks.extend(this_tasks)

    tasks = []
    solved_tasks = 0
    print_good_info("Scanning solved tasks...")
    for t in temp_tasks:
        this_path = t["path"]
        data_file = os.path.join(this_path, "text.txt")
        if not os.path.exists(data_file):
            tasks.append(t)
        else:
            solved_tasks += 1

    print_props(f"{solved_tasks} of {len(temp_tasks)} tasks are already solved!", console_color.BOLD, console_color.PURPLE)
    print_good_info("Tasks are generated!")
    return tasks

def check_existing_files(files : list):
    ex_counter = 0
    for i in files:
        if os.path.exists(i):
            ex_counter += 1

    print_props(f"{ex_counter} files exist ({ex_counter / len(files)} %)", console_color.DARKCYAN)


def download_all_artworks():
    downloading_threads = 200
    tasks = generate_tasks()
    print_props("Tasks total: " + str(len(tasks)), console_color.CYAN, console_color.BOLD)

    # paths = [task["path"] for task in tasks]
    # check_existing_files(paths)
    # make_all_dirs(paths)
    # print_good_info("Made all dirs!")

    task_sets = distribute_tasks(tasks, downloading_threads)
    print_good_info("Tasks are distributed!")

    loading_controller.init(target_tasks=len(tasks), update_probability=0.05)
    thread_solve(task_sets, thread_loader)

    print_good_info("All tasks finished!")
    print_red(f"During process {error_counter} errors occurred of all {len(tasks)} files")



if __name__ == '__main__':
    download_all_artworks()
