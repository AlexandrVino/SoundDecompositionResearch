import logging

import matplotlib.pyplot as plt
import numpy as np

from __config__ import PROCESSED, RAW
from utils.__main__ import update_config
from utils.math_transformations.integrals import f
from utils.math_transformations.least_squares import solve_least_squares_chart
from utils.charts.__main__ import build_charts_from_dir, get_png_file_name, need_to_build
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)
solution = {}
config_function = update_config()


def least_squares_chart(file_name, beautiful_name='', necessary=None):
    """
    :param file_name:
    :param beautiful_name:
    :param necessary: List of names songs necessary to build
    :return:
    """

    png_file_name = get_png_file_name(file_name, beautiful_name)
    # if not need_to_build(png_file_name, necessary):
    #     return

    log.info(f"Least Squares: Starting build {png_file_name}")

    (x, y, yn), coefficients = solve_least_squares_chart(file_name)

    config_function(
        png_file_name, least_square=coefficients, write=True
    )
    return

    log.info(f"Build chart {file_name}")
    plt.plot(x, y)
    plt.plot(x, yn, 'r')

    plt.title(beautiful_name)
    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    log.info(f"Save chart {file_name}")
    plt.savefig(f"{PROCESSED}/least_squares/{png_file_name}")

    # plt.show()
    plt.clf()

    log.info(f"End {file_name}")


if __name__ == '__main__':
    # least_squares_chart("classical_music/БЕТХОВЕН Лунная Соната.json")

    setup_matplotlib_text_color('black')
    setup_matplotlib(**{'font.size': '13'})

    build_charts_from_dir(
        f"{RAW}/wav",
        least_squares_chart,
        # file_names=get_file_data(f"{RAW}/songs_names.json")
    )
