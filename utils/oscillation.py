import json

from scipy.fft import fft, fftfreq

from __config__ import SOURCE_PATH, PROCESSED, RAW
from load import get_file_data
import logging
import matplotlib.pyplot as plt

from utils.chart_building import build_charts_from_dir
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config
import numpy as np
import os
import matplotlib as mpl

mpl.rcParams['agg.path.chunksize'] = 10000

args = setup_basic_config()
log = logging.getLogger(__name__)


def oscillation(file_name: str, beautiful_name: str = ''):
    """
    :param file_name: local path to filename
    :param beautiful_name: Beautiful name of the file
    :return: None

    Function for building charts of fourier processed data and save it
    """

    png_file_name = '/'.join([file_name.split('.')[0].split('/')[-2], beautiful_name]) \
        if beautiful_name else '/'.join(file_name.split('.')[0].split('/')[-2::])

    data_filename = png_file_name.split('.')[0].split('/')[1]
    folder = png_file_name.split('.')[0].split('/')[0]

    # log.info(f"Check if {png_file_name} in JSON")
    # with open(f'{PROCESSED}/songs_data_oscillation.json', 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    # if data_filename in data:
    #     if "oscillation_abs" in data[data_filename]:
    #         return

    need = ['wewillrockyou', 'Nothingelsematters', 'dabro', 'Луннаясоната', ]
    if not any(n.lower() in png_file_name.lower().replace(' ', '') for n in need):
        return

    log.info(f"Fourier Transform")
    log.info(f"Get data {file_name}")

    normalized_tone = get_file_data(file_name)

    n = len(normalized_tone)  # число точек
    sample_rate = 44100  # частота дискретизации

    log.info(f"Build axes {file_name}")
    yf = fft(normalized_tone)
    xf = fftfreq(n, 1 / sample_rate)

    step = len(xf) // 20000
    oscillation_list = []
    for x in range(0, len(xf), step):
        mini, maxi = min(yf[x:x + step]), max(yf[x:x + step])
        oscillation_list.append(abs(maxi - mini))
    oscillation_avg = sum(oscillation_list) / len(oscillation_list)

    # log.info(f"Save data {file_name}")
    # with open(f'{PROCESSED}/songs_data_oscillation.json', 'r', encoding='utf-8') as file:
    #     data = json.load(file)
    # print(oscillation_avg)
    # data[data_filename]["oscillation_abs"] = oscillation_avg
    # with open(f'{PROCESSED}/songs_data_oscillation.json', 'w', encoding='utf-8') as file:
    #     json.dump(data, file, indent=4, ensure_ascii=False)
    # return

    log.info(f"Build chart {file_name}")
    plt.text(0, 2.4 * 10 ** 7, f"w = {round(float(oscillation_avg), 3)}",
             bbox={'facecolor': 'green', 'edgecolor': 'black', 'boxstyle': ' round '
                   })

    plt.plot(np.clip(xf, 0, sample_rate // 2 + 1), np.clip(np.abs(yf), 0, 2.5 * 10 ** 7))  # с масштабом
    # plt.plot(np.clip(xf, 0, sample_rate // 2 + 1), np.abs(yf))  # без масштаба

    plt.title(beautiful_name)
    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    log.info(f"Save chart {file_name}")
    plt.savefig(f"{PROCESSED}/oscillation/{png_file_name}", transparent=True)

    plt.show()
    plt.clf()

    log.info(f"End {file_name}")


def solution_for_genres():
    log.info("Open songs_data_oscillation.json")
    with open(f'{PROCESSED}/songs_data_oscillation.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    solution = {
        "classical_music": [],
        "metal": [],
        "other": [],
        "rock": []
    }
    for value in data.values():
        solution[value["folder"]].append(value["oscillation"])

    log.info("Solve avg")
    for key, value in solution.items():
        solution[key] = sum(value) / len(value)

    log.info("Write solution")
    with open(f'{PROCESSED}/oscillation.json', 'w', encoding='utf-8') as file:
        json.dump(solution, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    setup_matplotlib_text_color('black')
    setup_matplotlib(**{'font.size': '13'})

    build_charts_from_dir(
        f"{PROCESSED}/json",
        oscillation,
        file_names=get_file_data(f"{RAW}/songs_names.json")
    )

    # solution_for_genres()
