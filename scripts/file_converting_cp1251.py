import os

base_path_out = "/cp1251_res"
base_path_in = "/\\"

file_list = [
    "author_page_links.json",
    "author_pages.json",
    "author_pages_data.json",
    "wiki_data.json",
]

file_list_in = []
file_list_out = []

for i in range(len(file_list)):
    file_list_in.append(os.path.join(base_path_in, file_list[i]))

for i in range(len(file_list)):
    file_list_out.append(os.path.join(base_path_out, file_list[i]))

print(file_list_in, file_list_out)

for filename_index in range(len(file_list_in)):
    in_file_bin = open(file_list_in[filename_index], "rb")
    out_file_data = in_file_bin.read().decode("utf8").encode("cp1251", errors = "ignore")
    in_file_bin.close()

    out_file = open(file_list_out[filename_index], "wb")
    out_file.write(out_file_data)
    out_file.close()


