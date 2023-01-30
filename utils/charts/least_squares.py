import logging

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

from __config__ import PROCESSED, RAW
from utils.charts.config import SAMPLE_RATE

from utils.charts.fourier_transform import solve_fourier_transform
from utils.charts.main import build_charts_from_dir, get_png_file_name, need_to_build
from utils.files.load import get_file_data
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def avg(data):
    return sum(data) / len(data)


def fun(a, x, y):
    return a[0] + a[1] * x + a[2] * x ** 2 - y


def least_squares_chart(file_name, beautiful_name='', necessary=None):
    """
    :param file_name:
    :param beautiful_name:
    :param necessary: List of names songs necessary to build
    :return:
    """

    png_file_name = get_png_file_name(file_name, beautiful_name)
    if not need_to_build(png_file_name, necessary):
        return

    log.info(f"Least Squares: Starting build {png_file_name}")

    x, y = solve_fourier_transform(file_name)
    x, y = (
        np.clip(x, 0, SAMPLE_RATE // 2 + 1),
        np.clip(y, 0, 2.5 * 10 ** 7)
    )

    step = 100
    x_1, y_1 = [], []
    for i in range(step, len(x), step):
        x_1.append(max(x[i - step:i]))
        y_1.append(max(y[i - step:i]))

    x, y = np.array(x_1), np.array(y_1)
    a0 = np.array([0, 0, 0])

    log.info(f"Call least_squares {png_file_name}")
    res_lsq = least_squares(fun, x0=a0, args=(x, y))

    f = lambda x: sum([u * v for u, v in zip(res_lsq.x, [1, x, x ** 2])])

    x_p = np.linspace(min(x), max(x), 50)
    y_p = f(x_p)
    plt.plot(x, y)
    plt.plot(x_p, y_p, 'r')

    plt.title(beautiful_name)
    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    plt.savefig(f"{PROCESSED}/least_squares/{png_file_name}", transparent=True)

    plt.show()
    plt.clf()

    log.info(f"End {png_file_name}")


if __name__ == '__main__':
    # least_squares_chart("classical_music/БЕТХОВЕН Лунная Соната.json")

    setup_matplotlib_text_color('black')
    setup_matplotlib(**{'font.size': '13'})

    build_charts_from_dir(
        f"{PROCESSED}/json",
        least_squares_chart,
        file_names=get_file_data(f"{RAW}/songs_names.json")
    )
