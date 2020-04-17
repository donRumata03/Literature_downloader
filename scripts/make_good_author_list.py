from lib.mylang import *

res = []
for author in from_utf8_json_file("D:\\Projects\\Literature_downloading\\wiki_data.json"):
    res.append(author["name"])

encoded = "\n".join(res).encode("cp1251")

out_filename = "D:\\Projects\\Literature_downloading\\cp1251_res\\good_author_names.txt"
out_file = open(out_filename, "wb")
out_file.write(encoded)
out_file.close()
