from lib.mylang import *

base_dir = "D:\\Literature_data\\All_books"

author_dirs = full_lsdir(base_dir)
res = []

bad_counter = good_counter= 0

print_good_info(f"Total authors: {len(author_dirs)}")
for author_index, author_dir in enumerate(author_dirs):
    author_name = os.path.split(author_dir)[1]
    author_obj = { "name" : author_name, "path" : author_dir, "artworks" : [] }
    for artwork_path in full_lsdir(author_dir):
        artwork_name = os.path.split(artwork_path)[1]
        artwork_obj = {"name": artwork_name, "folder_path": artwork_path, "author_name": author_name,
                       "author_path": author_dir, "size": 0}
        if os.path.exists(os.path.join(artwork_path, "text.txt")):
            artwork_obj["file_name"] = os.path.join(artwork_path, "text.txt")
            artwork_obj["size"] = os.stat(os.path.join(artwork_path, "text.txt")).st_size
            good_counter += 1
        else:
            bad_counter += 1

        author_obj["artworks"].append(artwork_obj)
    res.append(author_obj)
    if random.random() <= 0.001:
        print(f"Loading percent: {100. * author_index / len(author_dirs)} %")

print("\n\nBad percent:", 100. * bad_counter / (good_counter + bad_counter), "%")

res_file = r"D:\Projects\Literature_parser\system\best_book_data.json"

to_write = json.dumps(res, indent = 4, ensure_ascii = False).encode("cp1251", errors = "ignore")
open(res_file, "wb").write(to_write)
