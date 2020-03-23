from matplotlib import pyplot as plt
import json
import numpy as np


def normal(x, mu, m_sigma):
    return 1 / (m_sigma * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * m_sigma ** 2))

filename = "../res/Best_author_temp/Best_authors_temp_6666.json"

data = json.loads(open(filename, "r", errors='ignore', encoding="utf-8").read())

max_age = 0
min_age = 200

None_count = 0

print(len(data), "Authors")
min_author = None
max_author = None

for author in data:
    if author["wiki"]["life"]["age"] is None:
        None_count += 1
    else:
        if min_age > author["wiki"]["life"]["age"]:
            min_author = author["name"]
        if max_age < author["wiki"]["life"]["age"]:
            max_author = author["name"]

        max_age = max(max_age, author["wiki"]["life"]["age"])
        min_age = min(min_age, author["wiki"]["life"]["age"])




print("None percent:", 100 * None_count / len(data))

print("Max age:", max_age, "from author:", max_author)
print("Min age:", min_age, "from author:", min_author)


ms = [0 for i in range(max_age + 1)]

sigma = 1.

for author in data:
    age = author["wiki"]["life"]["age"]

    for i in range(len(ms)):
        ms[i] += normal(age, i, sigma)

plt.plot(list(range(len(ms))), ms)
plt.show()

