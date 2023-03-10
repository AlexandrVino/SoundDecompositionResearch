import logging

import numpy as np
from scipy.optimize import least_squares

from utils.charts.config import SAMPLE_RATE
from utils.charts.fourier_transform import solve_fourier_transform
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)
solution = {}


def avg(data):
    return sum(data) / len(data)


def fun(a, x, y):
    return a[0] + a[1] * x + a[2] * x ** 2 - y


def solve_least_squares_chart(file_name):
    """
    :param file_name:
    :return:
    """

    log.info(f"Least Squares: Starting solve {file_name}")

    x, y = solve_fourier_transform(file_name)
    x, y = (
        np.clip(x, 0, SAMPLE_RATE // 2 + 1),
        np.clip(y, 0, 2.5 * 10 ** 7)
    )

    step = 100
    data = np.array([
        np.array([avg(y[i - step:i]), avg(x[i - step:i])])
        for i in range(step, len(x), step)]
    )

    x, y = data[:, 0], data[:, 1]
    res_lsq = least_squares(fun, x0=np.array([0, 0, 0]), args=(x, y))

    return (x, y), res_lsq

