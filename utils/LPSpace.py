import json

import numpy as np

from __config__ import PROJECT_SOURCE_PROCESSED, PROJECT_SOURCE_RAW
from utils.chart_building import build_chart, build_charts_from_dir
from utils.least_squares import least_squares_chart
from utils.load import get_file_data


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


def solve_integral(function: str) -> str:
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
    if already_solved:
        integral = function
    else:
        integral = solve_integral(function)
    sm = 0
    for x in values:
        sm += eval(integral.replace('x', str(x)))
    return sm


def solve_for_data():
    with open(f"{PROJECT_SOURCE_PROCESSED}/songs_data.json", encoding='utf8') as input_file:
        data = json.load(input_file)
        frequencies = np.arange(0, 25000, 1)
        integ = solve_integral('ax^2 + bx + c')
        ans = []
        for key, value in data.items():
            c, b, a = map(lambda x: str(round(x, 5)), value['least_squares'])
            curr_integ = integ.replace('a', a).replace('b', b).replace('c', c)
            print(key, ":", curr_integ)
            ans.append(
                (
                    key,
                    solve_lp_for_function(curr_integ, frequencies, already_solved=True) / 1e12
                )
            )
    return sorted(ans, key=lambda x: x[-1])


def return_genres():
    normalized_genres = {
        (0, 450): 'classical',
        (600, 1400): 'rock',
        (1490, 2160): 'metal',
        (1450, 2000): 'other',
    }
    data = solve_for_data()
    print(*data, sep='\n')
    print()
    print()
    ans = []
    for name, value in data:
        for (tone_mn, tone_mx), genre in normalized_genres.items():
            if tone_mn < value < tone_mx:
                ans.append(f"{name} is a composition of {genre}")
                break
        else:
            ans.append(f"{name} is a composition of unknown genre")

    return ans


def add_musical_composition(filename):
    least_squares_chart(filename)


add_musical_composition(
    f"{PROJECT_SOURCE_RAW}/mp3/other/Geri Halliwell - It's Raining Men.mp3"
)
print('\n'.join(return_genres()))
