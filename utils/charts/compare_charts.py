import logging
import os

import matplotlib.pyplot as plt

from __config__ import PROCESSED, RAW
from utils.charts.config import COLORS, NAMES, SONGS_DATA
from utils.files.load import get_file_data
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def f(x: int, a: list[int]) -> int:
    return round(a[0] * x ** 2 + a[1] * x + a[2])


def find_song_names(directory='all'):
    """
    :param directory: all / each / directory_name
    """
    songs_names = get_file_data(f"{RAW}/songs_names.json")
    data = list()

    dir_name = f"{PROCESSED}/json"
    for dir in os.listdir(dir_name):
        if dir.endswith('.py'):
            continue

        for file in os.listdir(dir_name + '/' + dir):
            if file.endswith('.py'):
                continue

            name = (
                songs_names[file.split('.')[0]] if file.split('.')[0] in songs_names else
                '/'.join(file.split('.')[0].split('/')[-2::])
            )

            if directory == 'each':
                data.append([file, name, dir])
                break
            elif directory in {dir, 'all'}:
                data.append([file, name, dir])
            else:
                break

    already, average, integrals = [], {}, {}

    fig, ax = plt.subplots()
    for elem in data:
        build_one_chart(*elem, ax=ax, already=already, average=average, integrals=integrals)

    # ax.tick_params(color='white', labelcolor='white')
    # for spine in ax.spines.values():
    #     spine.set_edgecolor('white')
    ax.legend()

    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    plt.savefig(f"{PROCESSED}/least_squares/compare_charts.png", transparent=True)

    return average


def build_one_chart(
        file_name: str, beautiful_name: str, origin: str, ax: plt.Axes,
        already: list, average: dict, integrals: dict):
    log.info(f'Build {file_name}')

    if beautiful_name not in SONGS_DATA:
        log.info(f'No file data {file_name}')
        return -1

    coefficients = SONGS_DATA[beautiful_name]['least_squares']

    if not NAMES[origin] in already:
        kwargs = dict(label=NAMES[origin])
        already.append(NAMES[origin])

    if not average.get(origin):
        average[origin] = []

    average[origin].append(solve_one_integral(beautiful_name, coefficients)[1])
    integrals[beautiful_name] = average[origin][-1]

    ax.plot([f(x, coefficients) for x in range(25000)], COLORS[origin], **kwargs)


if __name__ == '__main__':
    #
    # solution(integrals_solution)
    setup_matplotlib_text_color('black')
    setup_matplotlib(**{'font.size': '13'})
