import logging

import numpy as np
from scipy.optimize import least_squares, leastsq

from utils.charts.config import SAMPLE_RATE
from utils.charts.fourier_transform import solve_fourier_transform
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)
solution = {}


def f(x, a, b, c):
    return a * x ** 2 + b * x + c


def residual(p, x, y):
    return y - f(x, *p)


def avg(data):
    return sum(data) / len(data)


def solve_least_squares_chart(file_name):
    """
    :param file_name:
    :return:
    """

    log.info(f"Least Squares: Starting solve {file_name}")

    log.info(f"Build axes {file_name}")
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

    log.info(f"Call least_squares {file_name}")
    coefficients, _ = list(leastsq(residual, np.array([1., 1., 1.]), args=(x, y)))

    yn = f(x, *coefficients)
    log.info(f"Call least_squares {file_name}")

    return (x, y, yn), coefficients
