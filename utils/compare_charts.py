import os
from __config__ import PROJECT_SOURCE_PROCESSED, PROJECT_SOURCE_RAW
from utils.load import get_file_data
import matplotlib.pyplot as plt
import logging

from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)

colors = {
        'classical_music': 'green',
        'metal': 'blue',
        'other': 'red',
        'rock': 'darkblue'
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

    for elem in data:
        build_one_chart(*elem)

    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')
    plt.savefig(f"{PROJECT_SOURCE_PROCESSED}/least_squares/compare_charts_1.png")
    plt.show()


def build_one_chart(file_name, beautiful_name, origin):
    log.info(f'Build {file_name}')

    if beautiful_name not in songs_data:
        log.info(f'No file data {file_name}')
        return -1

    a = songs_data[beautiful_name]['least_squares']
    plt.plot([f(x, a) for x in range(25000)], colors[origin])


if __name__ == '__main__':
    find_song_names('all')
