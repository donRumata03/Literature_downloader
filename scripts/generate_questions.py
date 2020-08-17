from lib.mylang import *

data = from_utf8_json_file(r"D:\Projects\Literature_downloading\res\wiki_data.json")
data.sort(key = lambda a: 0 if not a["wiki_data"]["life"]["precision"] else -len(a["artworks"]))

author_number = 10000
birth_pairs = []
art_pairs = []
for i in range(author_number):
    author = data[i]
    if author["wiki_data"]["life"]["precision"] is False:
        print("Too much authors")
        break
    birth_pairs.append((" ".join(reversed(author["name"].split())), author["wiki_data"]["life"]["birth_day"]))
    art_pairs.append((birth_pairs[-1][0], len(author["artworks"])))

out_fname = "C:\\Users\\Vova\\Documents\\author_birthdays.txt"
fout = open(out_fname, "w")

female_counter = 0

for i in range(len(birth_pairs)):
    if birth_pairs[i][0].split()[0][-1] == "а":
        birth_word = "родилась"
        write_word = "написала"
        female_counter += 1
        print(birth_pairs[i][0], "is female! Very bad!")
    else:
        birth_word = "родился"
        write_word = "написал"

    fout.write(f"В каком году {birth_word} {birth_pairs[i][0]}?\nВ {birth_pairs[i][1]}-ом году.\n_________________________________________________\n")
    fout.write(f"Сколько произведений {write_word} {birth_pairs[i][0]}?\n{art_pairs[i][1]} штук.\n_________________________________________________\n")

fout.close()

print(f"Total females: {female_counter} of {len(birth_pairs)} ({round(100 * female_counter / len(birth_pairs), 4)}%)")


