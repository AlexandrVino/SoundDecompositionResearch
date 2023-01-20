import json

import numpy as np

from __config__ import PROJECT_SOURCE_PROCESSED


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
            sm += (" + " if sm else "") + f'{koef}*(x ** ({degree + 1}) / {degree + 1})'
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


with open(f"{PROJECT_SOURCE_PROCESSED}/songs_data.json", encoding='utf8') as input_file:
    data = json.load(input_file)
    frequencies = np.array(np.arange(0, 25000, 10))
    integ = solve_integral('ax^2 + bx + c')
    ans = []
    for key, value in data.items():
        a, b, c = value['least_squares']
        ans.append((key, abs(solve_lp_for_function(
            integ.replace('a', str(a)).replace('b', str(b)).replace('c', str(c)),
            frequencies,
            already_solved=True
        )) / 1e22))
print(*sorted(
    ans, key=lambda x: x[-1]
), sep='\n')
