from collections import Counter

from matplotlib import pyplot as plt
import json
import numpy as np

from lib.graphic_smoother import smooth_graph, combi_smoothing
from lib.mylang import *

def normal(x, mu, m_sigma):
    return 1 / (m_sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * m_sigma ** 2))

filename = "../res/wiki_rate_temp/last_res.json"

data = json.loads(open(filename, "r", errors='ignore', encoding="utf-8").read())

max_date = 0
min_date = 3000

None_count = 0

print(len(data), "Authors")
min_author = None
max_author = None

bad_precision_counter = 0
not_alive_counter = 0

birth_days = []

for author in data:

    if author["wiki_data"]["life"]["birth_day"] is None:
        None_count += 1
        continue
    if not author["wiki_data"]["life"]["precision"]:
        bad_precision_counter += 1
        continue

    if not author["wiki_data"]["life"]["alive"]:
        not_alive_counter += 1
    else:
        birth_day = author["wiki_data"]["life"]["birth_day"]
        if min_date > birth_day:
            min_author = author["name"]
        if max_date < birth_day:
            max_author = author["name"]

        max_date = max(max_date, birth_day)
        min_date = min(min_date, birth_day)

        birth_days.append(birth_day)

print(np.array(sorted(birth_days)))


print("None percent:", 100 * None_count / len(data), "%")
print("Bad precision percent:", 100 * bad_precision_counter / len(data), "%")
print("Alive percent:", 100 * (1 - (not_alive_counter / len(data))), "%")

print("Max date:", max_date, "from author:", max_author)
print("Min date:", min_date, "from author:", min_author)

c = Counter(birth_days)


for_smoothing = [(i, c[i]) for i in list(c)]
print(for_smoothing)
smoothed = smooth_graph(for_smoothing, 0.4, combi_smoothing, 1000)

plot_tuple_graph(for_smoothing)
plt.show()

"""
min_val = min_date - 100
ms = [0 for i in range(min_val, max_date + 100)]

sigma = 20.

for author in data:
    date = author["wiki_data"]["life"]["birth_day"]

    for i in range(len(ms)):
        ms[i + min_val] += normal(date, i, sigma)
"""

# plt.plot(list(range(len(ms))), ms)
# plt.show()

