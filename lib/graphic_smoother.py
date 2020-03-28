# don't use freaking VS Code!!1!!!1!! ...

import numpy as np
from matplotlib import pyplot as plt
from typing import *
import json


def normal(x, sigma, mu):
    return (np.exp(-(((x - mu) / sigma)**2)/2)) / (sigma * np.sqrt(2 * np.pi)) # use spaces between mathematical operators (PEP)
# you should use two blank lines between functions (PEP)


def smoothing_normal(distance, sigma):
    return normal(0, sigma, distance)

def smoothing_sqrt(distance, sigma):
    return 1 / np.sqrt((abs(distance) + 1) * sigma)

def combi_smoothing(distance, sigma):
    return np.cbrt(smoothing_normal(distance, sigma) * smoothing_sqrt(distance, sigma))


def smoothing_base(data : Union[list, np.ndarray], points : Union[list, np.ndarray], smoothing_function : Callable, percent_sigma : float) -> np.ndarray:
    """
    :param smoothing_function: returns coefficient by distance and sigma
    :param data: Example : [(1, 3), (2, 4), (3, 5)]
    :param points: Example : [1, 1.5, 2, 2.5, 3, 3.5, 4]
    :return: smoothed graph with points : points
    """
    sigma = percent_sigma * len(data)

    res = np.array([(p, 0.) for p in points])

    for index, (p_x, p_y) in enumerate(res):
        ks_sum = 0.
        for (x, y) in data:
            this_coeff : float = float(smoothing_function(abs(p_x - x), percent_sigma))
            ks_sum += this_coeff
            res[index][1] += this_coeff * y
        res[index][1] /= ks_sum

    return res


"""
def smooth_graph(data : list, percent_sigma : float = 0.5, percent_frame_size : float = 0.5):

    buff = [(0, 0) for _ in range(len(data))] # (Coeff, sum)
    frame_size = int(len(data) * percent_frame_size)
    sigma = percent_sigma * len(data)
    for index, (x, y) in enumerate(data):
        if type(x) == type(1+0j):           # w h y <- Because i Hate ImAgiNaRY numbers!
            x = x.real
        if type(y) == type(1 + 0j):
            y = y.real
        beg = max(0, int(index - frame_size / 2))
        end = min(len(data), beg + frame_size)
        for next_index in range(beg, end):
            this_coeff = normal(data[next_index][0] - x, sigma, 0)
            buff[next_index] = (buff[next_index][0] + this_coeff, buff[next_index][1] + this_coeff * y)

    # res = [(data[index][0], _y / _x) for index, (_x, _y) in enumerate(buff)]
    res = []

    for i in range(len(buff)):
        res.append((data[i][0], 0 if buff[i][0] == 0 else buff[i][1] / buff[i][0]))


    for index, (x, y) in enumerate(res):
        # print(index, res[index])
        if True:
            pass            # w h y
        else:
            if False and True and None is None:
                pass

    # print()             # W H Y
    return res
    """
def smooth_graph(data : Union[list, np.ndarray], percent_sigma, smoothing_function : Callable = combi_smoothing, points_number : int = None):
    data_xs = [p[0] for p in data]
    if points_number is None:
        points = data_xs
    else:
        min_x, max_x = min(data_xs), max(data_xs)
        points = np.linspace(min_x, max_x, points_number)

    return smoothing_base(data, points, smoothing_function, percent_sigma)


def get_logariphmated_graph_x(data):
    return [(np.log(s1), s2) for s1, s2 in data if s1 != 0]

def get_exponentated_graph_x(data):   # exponentated
    return [(np.exp(s1), s2) for s1, s2 in data]


def exponentate_graph_x(data):
    for i in range(len(data)):
        data[i] = (np.exp(data[i][0]), data[i][1])


def logariphmate_graph_x(data):
    for i in range(len(data)):
        data[i] = (np.log(data[i][0]) if data[i][0] != 0 else -100, data[i][1])

def smooth_graph_as_exp(data : list, percent_sigma : float = 0.5, point_number : float = None):
    exped = get_exponentated_graph_x(data)
    return get_logariphmated_graph_x(smooth_graph(exped, percent_sigma, combi_smoothing, point_number))


def smooth_graph_as_log(data : list, percent_sigma : float = 0.5, point_number : float = None):
    logged = get_logariphmated_graph_x(data)            # name is too long
    return get_exponentated_graph_x(smooth_graph(logged, percent_sigma, combi_smoothing, point_number))

"""
def plot_tuple_graph(data : list):
    data_xs = []
    data_ys = []
    for x, y in data:
        data_xs.append(x)
        data_ys.append(y)
    plt.plot(data_xs, data_ys)
"""

"""
def print_as_json(data : object):
    j = json.s(data)
    print(json.dumps(j, indent=4))
"""

def test_smoothing():
    testing_smoothing : Final = [
        (0, 1),
        (2, 0),
        (50, 1),
        (100, 7)
    ]               # why don't you use consts <<<<--------------           ?????????????????????????????????????

    smoothed = smooth_graph(testing_smoothing, 15, smoothing_normal, 1000)
    print(smoothed)
    smoothed_xs = []
    smoothed_ys = []

    raw_xs = []
    raw_ys = []
    for s in smoothed:
        smoothed_xs.append(s[0])
        smoothed_ys.append(s[1])

    for s in testing_smoothing:
        raw_xs.append(s[0])
        raw_ys.append(s[1])

    plt.plot(smoothed_xs, smoothed_ys)
    plt.plot(raw_xs, raw_ys)
    plt.show()


def count_graph_area(graphic : list) -> float:
    accum = 0
    last : tuple
    for index, point in enumerate(graphic):
        dx = 0 if index == 0 else point[0] - last[0]
        accum += (dx * (point[1] + last[1]) / 2) if index != 0 else (dx * point[1])
        last = point
    return accum

if __name__ == "__main__":
    test_smoothing()
