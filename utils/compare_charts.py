import json
import os

import numpy as np

from __config__ import PROJECT_SOURCE_PROCESSED, PROJECT_SOURCE_RAW
from utils.load import get_file_data
import matplotlib.pyplot as plt
import logging
import matplotlib.patches as mpatches

from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)

colors = {
    'classical_music': '#21dec1',
    'metal': '#882bc3',
    'other': '#ff0000',
    'rock': '#0000fa'
}

names = {
    'classical_music': 'Классика',
    'metal': 'Метал',
    'other': 'Поп',
    'rock': 'Рок'
}

songs_data = get_file_data(f"{PROJECT_SOURCE_PROCESSED}/songs_data.json")


def f(x: int, a: list[int]) -> int:
    return round(a[0] * x ** 2 + a[1] * x + a[2])


def find_song_names(directory='all'):
    """
    :param directory: all / each / directory_name
    """
    songs_names = get_file_data(f"{PROJECT_SOURCE_RAW}/songs_names.json")
    if 'Ludovico Einaudi - Fly (megapesni' not in songs_names:
        print('lol')
    data = list()

    dir_name = f"{PROJECT_SOURCE_PROCESSED}/json"
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
    print(type(average))
    fig, ax = plt.subplots()
    for elem in data:
        build_one_chart(*elem, ax, already, average)
    ax.legend()

    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')
    plt.savefig(f"{PROJECT_SOURCE_PROCESSED}/least_squares/compare_charts_1.png")
    plt.show()
    return average


def build_one_chart(file_name, beautiful_name, origin, ax, already, average):
    log.info(f'Build {file_name}')

    if beautiful_name not in songs_data:
        log.info(f'No file data {file_name}')
        return -1
    a = songs_data[beautiful_name]['least_squares']

    kwargs = dict(label=origin)
    if kwargs['label'] in already:
        del kwargs['label']
    else:
        already.append(origin)

    y = [f(x, a) for x in range(25000)]
    if not average.get(origin):
        average[origin] = []
    average[origin].append(sum(y))

    ax.plot(y, colors[origin], **kwargs)


def solve(current: float, name):
    """
    :param current: current value of integral
    :param name: Title of composition
    :return:
    """

    with open(f'{PROJECT_SOURCE_PROCESSED}/integrals.json') as input_file:
        genres = json.load(input_file)

    with open(f'{PROJECT_SOURCE_PROCESSED}/solution.json', encoding='utf8') as input_file:
        solution = json.load(input_file)

    for key, value in genres.items():
        mn, mx = sorted([value, current])
        if not solution.get(name):
            solution[name] = {}
        solution[name][key] = round(mn / mx * 100, 2)

    sm = sum(solution[name].values())
    for key, value in solution[name].items():
        solution[name][key] = round(value / sm * 100, 2)

    with open(f'{PROJECT_SOURCE_PROCESSED}/solution.json', 'w', encoding='utf8') as output_file:
        json.dump(solution, output_file, indent=4, ensure_ascii=False)

    return ''


if __name__ == '__main__':
    plt.clf()
    average = list(map(lambda x: (x[0], sorted(x[1])), find_song_names('all').items()))
    data = []
    for i, (name, item_data) in enumerate(average):
        n = len(item_data)
        indexes = [n // 2, n // 2 + 1] if n % 2 == 0 else [n // 2]
        data.append(
            [float(round(sum(map(lambda x: item_data[x], indexes)) / len(indexes), 5)), names[name], colors[name]])

    items_data = np.array(data)
    items_names = items_data[:, 1]
    items_colors = np.array(items_data[:, 2])
    items_data = np.array(items_data[:, 0], dtype=np.float64)

    fig, ax = plt.subplots()

    for name, data, color in zip(items_names, items_data, items_colors):
        ax.bar([name], [data], color=color, label=name)
    ax.legend()
    ax.set_ylabel('Значение Интегралов')
    plt.ylim(0, max(items_data) + max(items_data) * 0.3)
    plt.savefig(f"{PROJECT_SOURCE_PROCESSED}/least_squares/integrals.png")
    plt.show()
