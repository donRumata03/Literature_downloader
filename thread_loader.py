from mylang import *
import urllib.request
import shutil

adecvatish_number = 10

class Artwork_loader(Thread):
    url = None
    resultive_path = "res/"
    index = None
    def __init__(self, url, index, res_path = "res/"):
        Thread.__init__(self)
        self.index = index
        self.url = url
        self.resultive_path = res_path
    def run(self):
        # Vova.silent_try_loading(urllib.request.urlretrieve, 3, self.url, "res/threads/unpacked/Thread_" + str(self.index) + "_result.zip")
        urllib.request.urlretrieve(self.url, "res/threads/unpacked/Thread_" + str(self.index) + "_result.zip")
        '''
        except Exception as e:
            ee = sys.exc_info()
            traceback.print_exception(*ee)
            print("Load ERROR!")
            print(self.url)
            print(self.resultive_path)
        '''
        shutil.unpack_archive("res/threads/unpacked/Thread_" + str(self.index) + "_result.zip", "res/threads/unpacked/Thread_" + str(self.index) + "/")

        largest = get_largest_txt_file_name("res/threads/unpacked/Thread_" + str(self.index))
        if largest is None:
            print("No txt files for " + self.resultive_path)
            return
        opened = open(largest, "rb")

        content = opened.read()
        file_to_write = open(self.resultive_path, "wb")
        file_to_write.write(content)
        file_to_write.close()


def multiprocess_load(urls : list, loader : Type, res_paths : list) -> None: # For each url there should be a corresponding path
    for dir_name in res_paths:
        mkdirs(dir_name)


    loaders = []

    for index, url in enumerate(urls):
        this_loader = loader(url, index, res_paths[index] + "\\text.txt")
        loaders.append(this_loader)

    works_to_say_to_perform = len(urls)

    ready = [0 for __ in range(len(loaders))]
    while True:
        alive_number = 0
        for index, loader in enumerate(loaders):
            if loader.is_alive():
                alive_number += 1
            else:
                if ready[index] == 1:
                    ready[index] = 2
        all_ready = True
        for i in ready:
            if i != 2:
                all_ready = False
                break
        if all_ready:
            return

        if alive_number < adecvatish_number:
            for new_thread_new_index in range(adecvatish_number - alive_number):
                this_thread = None
                if works_to_say_to_perform == 0:
                    return
                for i in range(len(ready)):
                    if ready[i] == 0:
                        ready[i] = 1
                        works_to_say_to_perform -= 1
                        this_thread = loaders[i]
                        this_thread.start()
        time.sleep(0.1)


if __name__ == "__main__":
    refs = ["https://royallib.com/get/txt/abbaszade_guseyn/belka.zip",
     "https://royallib.com/get/txt/abbaszade_guseyn/gudok_parohoda.zip",
     "https://royallib.com/get/txt/abbaszade_guseyn/dvernoy_molotok.zip",
     "https://royallib.com/get/txt/abbaszade_guseyn/komar.zip",
     "https://royallib.com/get/txt/abbaszade_guseyn/moy_drug_abdul.zip"]

    multiprocess_load(refs, Artwork_loader, [])
