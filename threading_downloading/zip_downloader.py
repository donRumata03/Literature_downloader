from lib.mylang import *
import urllib.request
import shutil
import os


def download_zip(link : str, filename : str, temporary_dir : str):
    proper_extension = "text.txt"
    if filename [-len(proper_extension):] != proper_extension:
        filename = os.path.join(filename, proper_extension)

    temp_folder = os.path.join(temporary_dir, hex(hash(link)).split("x")[-1])
    os.makedirs(temp_folder, exist_ok=True)
    urllib.request.urlretrieve(link, os.path.join(temp_folder, "result.zip"))
    shutil.unpack_archive(os.path.join(temp_folder, "result.zip"),
                          temp_folder)
    largest = get_largest_txt_file_name(temp_folder)
    shutil.copyfile(largest, filename)
    shutil.rmtree(temp_folder)




if __name__ == '__main__':
    # download_zip("https://royallib.com/get/txt/yatsenko_vladimir/desant_v_nastoyashchee.zip", "res/test/text.txt", "res/temp_test")

    e = 1.6e-19
    m_e = 0.9e-30

    k = 9 * 10**9
    import math
    mu = 1.26 * 10e-6
    U = 10_000

    print(k * 4 * math.pi * math.sqrt(m_e) / (mu * math.sqrt(2 * U * e)))


