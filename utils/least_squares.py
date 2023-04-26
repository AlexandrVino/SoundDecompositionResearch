import logging
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
from scipy.optimize import least_squares

from __config__ import PROCESSED, RAW
from utils.chart_building import build_charts_from_dir
from utils.load import get_file_data
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def avg(data):
    return sum(data) / len(data)


def fun(a, x, y):
    return a[0] + a[1] * x + a[2] * x ** 2 - y


def least_squares_chart(filename, beautiful_name=''):
    png_file_name = '/'.join([filename.split('.')[0].split('/')[-2], beautiful_name]) \
        if beautiful_name else '/'.join(filename.split('.')[0].split('/')[-2::])

    if os.path.exists(f"{PROCESSED}/least_squares/{png_file_name}.png"):
        pass

    need = ['wewillrockyou', 'Nothingelsematters', 'dabro', 'Луннаясоната', ]
    if not any(n.lower() in png_file_name.lower().replace(' ', '') for n in need):
        return

    log.info(f"Get data {filename[filename.find('source'):]}")

    normalized_tone = get_file_data(filename)

    n = len(normalized_tone)  # число точек
    sample_rate = 44100  # частота дискретизации

    log.info(f"Build axes {filename[filename.find('source'):]}")

    x = fftfreq(n, 1 / sample_rate)
    x = np.clip(x, 0, sample_rate // 2 + 1)
    y = fft(normalized_tone)
    y = np.clip(np.abs(y), 0, 2.5 * 10 ** 7)

    step = 100
    x_1, y_1 = list(), list()
    for i in range(step, len(x), step):
        x_1.append(max(x[i - step:i]))
        y_1.append(max(y[i - step:i]))
    x, y = np.array(x_1), np.array(y_1)

    a0 = np.array([0, 0, 0])

    log.info(f"Call least_squares {filename[filename.find('source'):]}")
    res_lsq = least_squares(fun, x0=a0, args=(x, y))
    print(res_lsq)

    log.info(f"Build chart {filename[filename.find('source'):]}")
    f = lambda x: sum([u * v for u, v in zip(res_lsq.x, [1, x, x ** 2])])
    x_p = np.linspace(min(x), max(x), 50)
    y_p = f(x_p)
    plt.plot(x, y)
    plt.plot(x_p, y_p, 'r')

    plt.title(beautiful_name)
    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    log.info(f"Save chart {filename[filename.find('source'):]}")
    plt.savefig(f"{PROCESSED}/least_squares/{png_file_name}", transparent=True)

    plt.show()
    plt.clf()

    log.info(f"End {filename[filename.find('source'):]}")


if __name__ == '__main__':
    # least_squares_chart("classical_music/БЕТХОВЕН Лунная Соната.json")

    setup_matplotlib_text_color('white')
    setup_matplotlib(**{'font.size': '13'})

    build_charts_from_dir(
        f"{PROCESSED}/json",
        least_squares_chart,
        file_names=get_file_data(f"{RAW}/songs_names.json")
    )
