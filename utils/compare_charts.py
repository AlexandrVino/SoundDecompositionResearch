import json
import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from __config__ import PROCESSED, RAW
from utils.load import get_file_data
from utils.matplotlibSetup import setup_matplotlib_font, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)

setup_matplotlib_text_color('white')
setup_matplotlib_font(**{'font.size': '13'})

COLORS = {
    'classical_music': '#21dec1',
    'metal': '#882bc3',
    'other': '#ff0000',
    'rock': '#0000fa'
}

NAMES = {
    'classical_music': 'Классика',
    'metal': 'Метал',
    'other': 'Поп',
    'rock': 'Рок'
}

songs_data = get_file_data(f"{PROCESSED}/songs_data.json")


def f(x: int, a: list[int]) -> int:
    return round(a[0] * x ** 2 + a[1] * x + a[2])


def find_song_names(directory='all'):
    """
    :param directory: all / each / directory_name
    """
    songs_names = get_file_data(f"{RAW}/songs_names.json")
    if 'Ludovico Einaudi - Fly (megapesni' not in songs_names:
        print('lol')
    data = list()

    dir_name = f"{PROCESSED}/json"
    for dir in os.listdir(dir_name):
        if dir.endswith('.py'):
            continue

        for file in os.listdir(dir_name + '/' + dir):
            if file.split('.')[0] in songs_names:
                name = songs_names[file.split('.')[0]]
            else:
                name = '/'.join(file.split('.')[0].split('/')[-2::])

            if file.endswith('.py'):
                continue
            elif directory == 'each':
                data.append([file, name, dir])
                break
            elif directory in {dir, 'all'}:
                data.append([file, name, dir])
            else:
                break

    already = []
    average = {}

    fig, ax = plt.subplots()
    for elem in data:
        build_one_chart(*elem, ax, already, average)

    ax.tick_params(color='white', labelcolor='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    ax.legend()

    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')
    plt.savefig(f"{PROCESSED}/least_squares/compare_charts_1.png", transparent=True)
    plt.show()
    return average


def build_one_chart(file_name, beautiful_name, origin, ax, already, average):
    log.info(f'Build {file_name}')

    if beautiful_name not in songs_data:
        log.info(f'No file data {file_name}')
        return -1
    a = songs_data[beautiful_name]['least_squares']

    kwargs = dict(label=NAMES[origin])
    if kwargs['label'] in already:
        del kwargs['label']
    else:
        already.append(NAMES[origin])

    y = [f(x, a) for x in range(25000)]
    if not average.get(origin):
        average[origin] = []
    average[origin].append(sum(y))

    ax.plot(y, COLORS[origin], **kwargs)


def solve(current: float, title):
    """
    :param current: current value of integral
    :param title: Title of composition
    :return:
    """

    with open(f'{PROCESSED}/integrals.json') as input_file:
        genres = json.load(input_file)

    with open(f'{PROCESSED}/solution.json', encoding='utf8') as input_file:
        solution = json.load(input_file)

    for key, value in genres.items():
        mn, mx = sorted([value, current])
        if not solution.get(title):
            solution[title] = {}
        solution[title][key] = round(mn / mx * 100, 2)

    sm = sum(solution[title].values())
    for key, value in solution[title].items():
        solution[title][key] = round(value / sm * 100, 2)

    with open(f'{PROCESSED}/solution.json', 'w', encoding='utf8') as output_file:
        json.dump(solution, output_file, indent=4, ensure_ascii=False)


def plot_average_integrals():
    plt.clf()

    average = list(map(lambda x: (x[0], sorted(x[1])), find_song_names('all').items()))
    data = []
    for genre, item_data in average:
        n = len(item_data)
        indexes = [n // 2, n // 2 + 1] if n % 2 == 0 else [n // 2]

        data.append(
            [
                round(sum(map(lambda x: item_data[x], indexes)) / len(indexes), 5),
                NAMES[genre],
                COLORS[genre]
            ]
        )
    print(data)
    items_data = np.array(data)
    fig, ax = plt.subplots()

    for (data, name, color) in items_data:
        ax.bar([name], [float(data)], color=color, label=name)

    ax.tick_params(color='white', labelcolor='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    ax.legend()
    ax.set_ylabel('Значение Интегралов')
    ax.legend()

    plt.ylim(0, max(np.array(items_data[:, 0], dtype=np.float)) * 1.3)
    plt.savefig(f"{PROCESSED}/least_squares/integrals.png", transparent=True)
    plt.show()


if __name__ == '__main__':
    plot_average_integrals()
