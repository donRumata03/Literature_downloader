from lib.mylang import *
from threading import Thread

class Plotter(Thread):
    xs = []
    ys = []
    def __init__(self, xs, ys):
        Thread.__init__(self)
        self.xs = xs
        self.ys = ys
    def run(self):

        plt.plot(self.xs, self.ys)
        plt.show()

def glue_thread_files(filenames : list, target_file : str):
    datas = []
    for index, filename in enumerate(filenames):
        print(100 * index / len(filenames), "%")
        datas.append(load_json_from_file(filename))
    res = []
    for data in datas:
        res.extend(data)
    save_as_json(res, target_file)

def build_num_of_artworks_graph():
    distribution = make_atr_distribution()

    plt.plot(distribution)
    plt.show()


def make_atr_distribution():
    data = load_json_from_file("../All_authors_artworks.json")
    plot_xs = []
    plot_ys = []
    max_arts = 0
    max_author = ""
    for author in data:
        val = len(author["artworks"])
        if val > max_arts:
            max_arts = val
            max_author = author["name"]
    print("Max author :", max_author, f"with {max_arts} arts")
    distribution = [0 for _ in range(max_arts + 1)]
    for author in data:
        val = len(author["artworks"])
        distribution[val] += 1
    return distribution


def integrate_distribution(num : int, d):
    distribution = d if d is not None else make_atr_distribution()
    res = 0
    index = 0
    for i in distribution[num:]:
        res += i
        index += 1
    return res

def integrate_distribution_with_multiplication(num : int, d):
    distribution = d if d is not None else make_atr_distribution()
    res = 0
    index = 0
    for i in distribution[num:]:
        res += i * index
        index += 1
    return res


def show_integral():
    xs = []
    ys = []
    ys2 = []
    d = make_atr_distribution()
    for this_index in range(len(d)):
        xs.append(this_index)
        ys.append(integrate_distribution(this_index, d))
        ys2.append(integrate_distribution_with_multiplication(this_index, d))
    t1 = Plotter(xs, ys2)
    t1.start()
    t1.join()


def convert_all_files_to_cp1251(dir_name : str, out_dir_name : str):
    d = full_lsdir(folder_name=dir_name)
    dd = os.listdir(dir_name)
    for index, val in enumerate(d):
        convert_file_to_cp1251(d[index], out_dir_name + dd[index])


def get_conged_json_file(dir_name : str):
    datas = []
    filenames = full_lsdir(dir_name)
    for index, filename in enumerate(filenames):
        print(100 * index / len(filenames), "%")
        datas.append(load_json_from_file(filename))
    res = []
    for data in datas:
        res.extend(data)

    return res

def count_all_size_bytes(all_json : list):
    res = 0
    for author in all_json:
        arts = author["artworks"]
        if len(arts) < 2:
            continue
        for art in arts:
            if "page_data" in art:
                page_data = art["page_data"]
                if "size" in page_data and page_data["size"]:
                    res += page_data["size"]
                else:
                    pass
                    # print_red("No info here:" + str(author))

    print_good_info(res, "Bytes TOTAL")
    print_good_info(res / 1024, "KiloBytes TOTAL")
    print_good_info(res / (1024 * 1024), "MegaBytes TOTAL")
    print_good_info(res / (1024 * 1024 * 1024), "GigaBytes TOTAL")


def filter_good_authors(all_json : list, edge : int = 3):
    res = []
    for author in all_json:
        arts = author["artworks"]
        if len(arts) < edge:
            continue
        res.append(author)
    return res

def get_good_auth_jsn():
    all_json = get_conged_json_file("../res/thread_art_parse_results")
    # count_all_size_bytes(all_jsn)
    # all_json = load_json_from_file("res/download_test.json")
    return filter_good_authors(all_json)


if __name__ == "__main__":
    # glue_thread_files(full_lsdir("res/thread_art_parse_results"), "All_artworks_data.json")
    # convert_all_files_to_cp1251("res/thread_art_parse_results", "res/art_parse_temp")
    print(get_life_time("Dfdlkdsfgljk 123423 34 1111 1213"))
    all_jsn = get_conged_json_file("../res/thread_art_parse_results")
    count_all_size_bytes(all_jsn)
    # show_integral()
