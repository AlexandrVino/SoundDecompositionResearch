import json

from scipy import integrate

from __config__ import PROCESSED
from utils.files.load import get_file_data


def f(x, a, b, c):
    return a * x ** 2 + b * x + c


def solve_integrate(args, frequencies_mn: int = 0, frequencies_mx: int = 25000):
    return integrate.quad(f, frequencies_mn, frequencies_mx, args=tuple(args))


def solve_for_data():
    data = get_file_data('songs_data.json')

    return {k: v for k, v in sorted([
        (key, solve_integrate(value['least_squares'])[0])
        for key, value in data.items()
    ], key=lambda x: x[-1])}


def solve_for_composition(genres, sol, current, title):
    genre = title.split('/')[0]
    print(genre)
    for key, value in genres.items():
        mn, mx = sorted([value, current])
        if not sol.get(genre):
            sol[genre] = {}
        sol[genre][key] = round(mn / mx * 1000, 2)

    sm = sum(sol.get(genre, {}).values())
    for key, value in sol[genre].items():
        sol[genre][key] = round(value / sm * 100, 2)


def solve(integrals_solution):
    with open(f'{PROCESSED}/integrals.json') as input_file:
        genres = json.load(input_file)

    with open(f'{PROCESSED}/solution.json', encoding='utf8') as input_file:
        sol = json.load(input_file)

    for title, value in integrals_solution.items():
        solve_for_composition(genres, sol, value, title)

    with open(f'{PROCESSED}/solution.json', 'w', encoding='utf8') as output_file:
        json.dump(sol, output_file, indent=4, ensure_ascii=False)


solve(solve_for_data())
