import json

from scipy import integrate

from __config__ import PROCESSED


def f(x, a, b, c):
    return a * x ** 2 + b * x + c


def solve_integrate(args, frequencies_mn: int = 0, frequencies_mx: int = 25000):
    return integrate.quad(f, frequencies_mn, frequencies_mx, args=args)


def solve_for_data():
    with open(f"{PROCESSED}/songs_data.json", encoding='utf8') as input_file:
        data = json.load(input_file)

    return sorted([
        solve_integrate(value['least_squares'])
        for key, value in data.items()
    ], key=lambda x: x[-1])


def solve_for_composition(genres, sol, current, title):
    for key, value in genres.items():
        mn, mx = sorted([value, current])
        if not sol.get(title):
            sol[title] = {}
        sol[title][key] = round(mn / mx * 1000, 2)

    sm = sum(sol[title].values())
    for key, value in sol[title].items():
        sol[title][key] = round(value / sm * 100, 2)


def solve(integrals_solution):
    with open(f'{PROCESSED}/integrals.json') as input_file:
        genres = json.load(input_file)

    with open(f'{PROCESSED}/solution.json', encoding='utf8') as input_file:
        sol = json.load(input_file)

    for title, value in integrals_solution.items():
        solve_for_composition(genres, sol, value, title)

    with open(f'{PROCESSED}/solution.json', 'w', encoding='utf8') as output_file:
        json.dump(sol, output_file, indent=4, ensure_ascii=False)
