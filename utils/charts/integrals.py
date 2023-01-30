import json

import numpy as np
from matplotlib import pyplot as plt

from __config__ import PROCESSED
from utils.charts.__config__ import COLORS, NAMES
from utils.charts.compare_charts import find_song_names


def prepare_function(function: str) -> str:
    """
    :param function: a polynomial of the form ax^n + bx^(n - 1)+ cx^(n - 2) + ... lx^0
    :return:  a polynomial of the form a*x**n + b*x**(n - 1)+ c*x**(n - 2) + ... l*x**0
    """

    function = function.replace('^', '**')
    for i in range(1, len(function)):
        if function[i] == 'x' and function[i - 1] in 'abc':
            return prepare_function(function[:i] + "*" + function[i:])

    return function


def solve_integrals(function: str) -> str:
    function = prepare_function(function).split(' + ')

    sm = ''
    for item in function:
        if 'x' in item:
            buff = item.split('**')
            degree = 1 if not buff[-1].isdigit() else int(buff[-1])
            buff = buff[0].split('*')
            koef = 1 if buff[0] == 'x' else buff[0]
            sm += (" + " if sm else "") + f'{koef}*((x ** {degree + 1}) / {degree + 1})'
        else:
            sm += (" + " if sm else "") + f'{item}*x'
    return sm


def solve_lp_for_function(function: str, values: np.ndarray, already_solved=False):
    integral = function if already_solved else solve_integrals(function)
    return sum(eval(integral.replace('x', str(x))) for x in values)


def solve_for_data():
    with open(f"{PROCESSED}/songs_data.json", encoding='utf8') as input_file:
        data = json.load(input_file)

    ans = []
    for key, value in data.items():
        ans.append(solve_one_integral(key, value['least_squares']))

    return sorted(ans, key=lambda x: x[-1])


def solve_one_integral(
        title: str, args: list, frequencies: np.ndarray = np.arange(0, 25000, 1),
        integral: str = solve_integrals('ax^2 + bx + c')):
    """
    :param title: title of song
    :param frequencies: range for directed integral
    :param integral: integral string
    :param args: coefficients P(x)
    :return:
    """

    a, b, c = map(lambda x: str(round(x, 5)), args)
    curr_integral = integral.replace('a', a).replace('b', b).replace('c', c)
    return (
        (
            title,
            round(
                solve_lp_for_function(
                    curr_integral,
                    frequencies,
                    already_solved=True
                )
            )
        )
    )


def solve(integrals_solution):
    with open(f'{PROCESSED}/integrals.json') as input_file:
        genres = json.load(input_file)

    with open(f'{PROCESSED}/solution.json', encoding='utf8') as input_file:
        sol = json.load(input_file)

    for title, value in integrals_solution.items():
        solve_for_composition(genres, sol, value, title)

    with open(f'{PROCESSED}/solution.json', 'w', encoding='utf8') as output_file:
        json.dump(sol, output_file, indent=4, ensure_ascii=False)


def solve_for_composition(genres, sol, current, title):
    for key, value in genres.items():
        mn, mx = sorted([value, current])
        if not sol.get(title):
            sol[title] = {}
        sol[title][key] = round(mn / mx * 1000, 2)

    sm = sum(sol[title].values())
    for key, value in sol[title].items():
        sol[title][key] = round(value / sm * 100, 2)


def plot_average_integrals():
    plt.clf()

    average = list(map(lambda x: (x[0], sorted(x[1])), find_song_names().items()))
    data = [
        [
            round(sum(item_data) / len(item_data), 5),
            NAMES[genre],
            COLORS[genre]
        ] for genre, item_data in average
    ]

    items_data = np.array(data)
    fig, ax = plt.subplots()

    for (data, name, color) in items_data:
        ax.bar([name], [float(data)], color=color)

    # ax.tick_params(color='white', labelcolor='white')
    # for spine in ax.spines.values():
    #     spine.set_edgecolor('white')

    ax.set_ylabel('Значение Интегралов')
    # ax.legend()

    plt.ylim(0, max(np.array(items_data[:, 0], dtype=np.float)) * 1.3)
    plt.savefig(f"{PROCESSED}/least_squares/integrals.png", transparent=True)
    plt.show()

