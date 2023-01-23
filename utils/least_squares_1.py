import json
import os
from scipy.optimize import leastsq
from scipy.fft import fft, fftfreq

import matplotlib.pyplot as plt
import numpy as np

from __config__ import PROJECT_SOURCE_PROCESSED, PROJECT_SOURCE_RAW
from utils.chart_building import build_charts_from_dir
from utils.load import get_file_data

from utils.my_argparse import setup_basic_config
import logging

from utils import fourier_transform

args = setup_basic_config()
log = logging.getLogger(__name__)


def f(x, a, b, c):
    return a * x ** 2 + b * x + c


def residual(p, x, y):
    return y - f(x, *p)


def least_squares_chart(filename, beautiful_name=''):

    png_file_name = '/'.join([filename.split('.')[0].split('/')[-2], beautiful_name]) \
        if beautiful_name else '/'.join(filename.split('.')[0].split('/')[-2::])

    data_filename = png_file_name.split('.')[0].split('/')[1]

    # if os.path.exists(f"{PROJECT_SOURCE_PROCESSED}/least_squares/{png_file_name}.png"):
    #     # return
    #     pass
    #
    data = json.load(open(f'{PROJECT_SOURCE_PROCESSED}/songs_data.json', 'r', encoding='utf-8'))
    if data_filename in data:
        log.info(f'Skip {filename}')
        return

    log.info(f"Get data {filename}")

    normalized_tone = get_file_data(filename)

    n = len(normalized_tone)  # число точек
    sample_rate = 44100  # частота дискретизации

    log.info(f"Build axes {filename}")
    x = fftfreq(n, 1 / sample_rate)
    x = np.clip(x, 0, sample_rate // 2 + 1)
    y = fft(normalized_tone)
    y = np.clip(np.abs(y), 0, 2.5 * 10 ** 7)

    step = 15000
    x_1, y_1 = list(), list()
    for i in range(step, len(x), step):
        x_1.append(max(x[i - step:i]))
        y_1.append(max(y[i - step:i]))
    x, y = np.array(x_1), np.array(y_1)

    log.info(f"Call least_squares {filename}")
    a = np.array([1., 1., 1.])
    c, len_c = list(leastsq(residual, a, args=(x, y)))
    yn = f(x, *c)

    log.info(f"Save data {filename}")
    with open(f'{PROJECT_SOURCE_PROCESSED}/songs_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data[data_filename] = {'least_squares': list(c)}
    with open(f'{PROJECT_SOURCE_PROCESSED}/songs_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    # return

    log.info(f"Build chart {filename}")
    plt.plot(x, y)
    plt.plot(x, yn, 'r')

    plt.title(beautiful_name)
    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    log.info(f"Save chart {filename}")
    plt.savefig(f"{PROJECT_SOURCE_PROCESSED}/least_squares/{png_file_name}")

    # plt.show()
    plt.clf()

    log.info(f"End {filename}")


if __name__ == '__main__':
    build_charts_from_dir(
        f"{PROJECT_SOURCE_PROCESSED}/json",
        least_squares_chart,
        file_names=get_file_data(f"{PROJECT_SOURCE_RAW}/songs_names.json")
    )
