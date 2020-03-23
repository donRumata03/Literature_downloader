# -*- coding: utf-8 -*-
import wikipedia
from matplotlib import pyplot as plt
import json
import wikipedia_worker
import winsound
import random
import time
from threading import Thread
import os
import sys
from typing import *
import traceback
from datetime import datetime

class console_color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def print_props(something, *props, end="\n"):
    for i in props:
        print(i, end="")
    print(str(something))
    for i in range(len(props)):
        print(console_color.END, end="")

    print(end, end="")

def print_good_info(*something, end : str = "\n", sep : str = " "):
    print_props(sep.join(map(str, something)), console_color.BOLD, console_color.GREEN, end=end)


def print_red(*something, end : str = "\n", sep : str = " "):
    print_props(sep.join(map(str, something)), console_color.RED, console_color.BOLD, end=end)


class Vova:
    thread = None
    Vova_negr = None
    def __init__(self):
        self.thread = Vovalic_thread()
    @staticmethod
    def silent_try_loading(internet_function, num = None, *args):
        while num is None or num:
            try:
                internet_function(*args)
            except Exception as e:
                if num == 1:
                    ei = sys.exc_info()
                    traceback.print_exception(*ei)
            if num is not None:
                num -= 1


    @staticmethod
    def pronounce_alert():
        winsound.PlaySound('sound.wav', winsound.SND_FILENAME)

    def multi_alert(self):
        self.thread.start()
        self.thread = Vovalic_thread()

    def try_loading(self, internet_function, args):
        if self.Vova_negr is None:
            self.Vova_negr = Vova()
        func_result = None
        exception_printed = set()
        while func_result is None:
            try:
                func_result = internet_function(args)
            except Exception as e:
                if e.__class__ not in exception_printed:
                    print("New exception caught!..", "Exception, what would you say before I kill you?..")
                    print('\033[91m')
                    e_info = sys.exc_info()
                    traceback.print_exception(*e_info)
                    print('\033[0m')
                    exception_printed.add(e.__class__)
                    time.sleep(0.1)
                    print("End of caught exception`s speech!!!")
                self.Vova_negr.multi_alert()
                time.sleep(10)
        self.Vova_negr = Vova()
        return func_result

    def lazy_try_loading(self, internet_function, num, args, delay_sec : float = 5.) -> Optional[Any]:
        if self.Vova_negr is None:
            self.Vova_negr = Vova()
        func_result = None
        exception_printed = set()
        counter = 1
        while func_result is None:
            try:
                func_result = internet_function(args)
            except Exception as e:
                if counter > num:
                    return None
                counter += 1
                if e.__class__ not in exception_printed:
                    print_props("New exception caught!..", "Exception, what would you say before I kill you?..", console_color.PURPLE, console_color.BOLD)
                    time.sleep(0.1)
                    print('\033[91m')
                    e_info = sys.exc_info()
                    traceback.print_exception(*e_info)
                    print('\033[0m')
                    exception_printed.add(e.__class__)
                    time.sleep(0.1)
                    print_props("End of caught exception`s speech!!!", console_color.PURPLE, console_color.BOLD)
                else:
                    print_props("Exception of known type caught", console_color.YELLOW, console_color.BOLD)

                self.Vova_negr.multi_alert()
                time.sleep(delay_sec)
        self.Vova_negr = Vova()
        return func_result


class Vovalic_thread(Thread):
    def __init__(self):
        Thread.__init__(self)
        pass
    def run(self):
        Vova.pronounce_alert()



def find_4_digit_nums(string : str) -> list:
    res = []
    this_number = []
    for char in string:
        if len(this_number) == 4:
            res.append(int("".join(this_number)))
        if char.isdigit():
            this_number.append(char)
        else:
            this_number = []
        if len(this_number) == 4:
            res.append(int("".join(this_number)))
    return res

def convert_file_to_cp1251(filename : str, output_file : str):
    file : str = open(filename, "r", encoding="utf8").read()
    decoded : bytes = file.encode("cp1251", errors="ignore")
    out = open(output_file, "wb")
    out.write(decoded)

def load_json_from_file(filename : str):
    file = open(filename, "r", encoding="utf8").read()
    return json.loads(file)

def save_as_json(something : object, filename):
    string = json.dumps(something, ensure_ascii=False, indent=4)
    file = open(filename, "w", encoding="utf-8")
    file.write(string)
    file.close()

def file_size(filename : str) -> int:
    st = os.stat(filename)
    return st.st_size

def full_lsdir(folder_name : str) -> list:
    res = os.listdir(make_good_filename(folder_name))
    for i in range(len(res)):
        res[i] = folder_name + "\\" + res[i]
    return res

def has_extension(filename, extension):
    return filename[-len(extension):] == extension

def get_largest_txt_file_name(base_path : str) -> Union[str, None] :
    file_names : list = os.listdir(base_path)
    txt_files = []
    for file in file_names:
        if has_extension(base_path + "\\" + file, ".txt"):
            txt_files.append(base_path + "\\" + file)
    if not txt_files:
        return None
    best_res = -1
    best_file = ""

    for txt_file in txt_files:
        this_size = file_size(txt_file)
        if best_res < this_size:
            best_res = this_size
            best_file = txt_file
    return best_file

def get_life_time(summary : str) -> dict:
    numbers = find_4_digit_nums(summary)
    if len(numbers) == 0:
        return {"success" : False, "age" : 50}

    born_date = numbers[0]
    if len(numbers) == 1:
        return {"success": False, "age": None, "born": born_date, "alive" : born_date > 2019 - 60 }

    # assume life is longer than 30 years
    # but shorter than 80
    end = None
    lifetime = -1
    for poss_date in numbers[1:]:
        lifetime = poss_date - born_date
        if 30 < lifetime < 80:
            end = poss_date
            break
    if end is not None:
        return {"success" : True, "age" : lifetime, "born" : born_date, "end" : end, "alive" : False}
    return { "success": False, "age": None, "born": born_date, "alive" : born_date > 2019 - 60 }

def clever_life(response : wikipedia.WikipediaPage, quick_table = None):
    res = {}

    if quick_table is None:
        quick_table = wikipedia_worker.get_quick_table(response.html())
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

def add_all(dict_to : dict, dict_from : dict) -> None:
    for key in dict_from:
        dict_to[key] = dict_from[key]

def del_nonletters(s : str) -> str:
    res = []
    for ch in s:
        if ch.isalnum() or ch == " ":
            res.append(ch)
    return "".join(res)

def print_as_json(data):
    string = json.dumps(data, ensure_ascii=False, indent=4)
    print(string)

def replace_all(string : str, chars : set, new_char : str = ""):
    res = []
    for this_char in string:
        if this_char in chars:
            res.append(new_char)
        else:
            res.append(this_char)
    return "".join(res)

# Splitting
def all_split(data : str, splitters : set) -> list:
    return split_if(data, lambda x: x in splitters)

def split_words(data : str):
    return split_if(data, lambda x: not x.isalnum())

def split_if(data : str, function) -> list:
    lst_dat = list(data)
    new_lstdat = []
    for char in lst_dat:
        if function(char):
            new_lstdat.append("♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥")
        else:
            new_lstdat.append(char)
    return "".join(new_lstdat).split("♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥")


def make_good_filename(start_path : str) -> str:
    splitted = all_split(start_path, {"/", "\\"})
    path = ""

    for i in range(len(splitted)):
        if i != 0:
            splitted[i] = replace_all(splitted[i], {".", ",", "!", ":", "'", "\"", "*", ">", "<", "|", "?"}, "")
        splitted[i] = splitted[i].strip()
        path += splitted[i]
        if i != len(splitted) - 1:
            path += "\\"
    return path

russians = ['ё', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

def is_russian(char : str):
    assert(len(char) == 1)
    return char in russians


def find_first_number(string : str):
    res = None
    counter = 0
    for s in string:
        if s.isdigit():
            res = s
            break
        counter += 1
    return counter

def find_first_not_number(string : str):
    res = None
    counter = 0
    for s in string:
        if not s.isdigit():
            res = s
            break
        counter += 1
    return counter if res is not None else None

def find_first_not_number_or_dot(string : str):
    res = None
    counter = 0
    for s in string:
        if not s.isdigit() and not (s == "."):
            res = s
            break
        counter += 1
    return counter if res is not None else None

def find_last_number(string : str) -> int:
    res = None
    counter = len(string) - 1
    for s in string[::-1]:
        if s.isdigit():
            res = s
            break
        counter -= 1
    return counter

def extract_int(string : str) -> Optional[int]:
    p1 = find_first_number(string)
    if p1 is None:
        return None
    p2 = find_first_not_number(string[p1:]) + p1
    for_num = string[p1 : p2]
    return int(for_num)

def extract_float(string : str) -> Union[float, None]:
    p1 = find_first_number(string)
    if p1 is None:
        return None
    p2 = find_first_not_number_or_dot(string[p1:]) + p1
    for_num = string[p1 : p2]
    return float(for_num)

def find_if(res : str, predicate : Callable, offset : int) -> Optional[int]:
    pos = offset
    while pos != len(res):
        if predicate(res[pos]):
            return pos
        pos += 1

    return None


def count_byte_size(size_description : str, debug = False) -> Optional[int]:
    number = extract_int(size_description)
    if number is None:
        return None
    pos = find_first_number(size_description)

    size_mapper = {
        "" :  1,
        "к" : 1024,
        "м" : 1024 * 1024,
        "г" : 1024 * 1024 * 1024,
        "т" : 1024 * 1024 * 1024 * 1024
    }

    size_description = size_description.lower()
    meaning_letter = size_description[find_if(size_description, lambda x: is_russian(x), pos)]
    size_multiplier = size_mapper[meaning_letter]

    if debug:
        print(number, pos, size_multiplier)

    res = size_multiplier * number

    return res

def mkdirs(path : str) -> str:
    splitted = all_split(path, {"/", "\\"})
    to_add = False
    if ":" in splitted[0]:
        to_add = True

    this_path = splitted[0]
    del splitted[0]
    if to_add:
        this_path += "\\"

    while splitted:
        if splitted[0] not in os.listdir(this_path):
            # print(splitted[0], this_path, os.listdir(this_path))
            this_path += splitted[0]
            if len(splitted) != 1:
                this_path += "\\"
            try:
                os.mkdir(this_path)
            except Exception as e:
                ex_info = sys.exc_info()
                traceback.print_exception(*ex_info)
                print(e)
        else:
            this_path += splitted[0] + "\\"
        del splitted[0]
    return path

def make_all_dirs(dirs : list):
    for directory in dirs:
        mkdirs(directory)

def make_non_existing_dirs(base : str, paths : List[str]):
    ld = full_lsdir(base)
    real_dirs_to_make = []
    for i in paths:
        if i not in ld:
            real_dirs_to_make.append(i)

    print(f"Making {len(real_dirs_to_make)}")
    make_all_dirs(real_dirs_to_make)


def recursive_lsdir(base_path: str) -> dict:
    os.walk

if __name__ == "__main__":
    paty = 'D:\\Projects\\Literature_analyzer\\res\\Books\\Loading\\Арджилли Марчелло\\Читай болван '
    print(paty.find(('Читай болван '.strip())))
    print_props("Hello, world!", console_color.CYAN, console_color.BOLD, console_color.UNDERLINE)
    print("Hello!")