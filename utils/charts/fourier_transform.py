import logging

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from __config__ import PROCESSED, RAW
from utils.charts.__main__ import build_charts_from_dir, get_png_file_name, need_to_build
from utils.charts.config import SAMPLE_RATE
from utils.files.load import get_file_data
from utils.math_transformations.fourier_transform import solve_fourier_transform
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

mpl.rcParams['agg.path.chunksize'] = 10000

args = setup_basic_config()
log = logging.getLogger(__name__)


def fourier_transform(file_name: str, beautiful_name: str = '', necessary=None):
    """
    :param file_name: local path to filename
    :param beautiful_name: Beautiful name of the file
    :param necessary: Beautiful name of the file
    :return: None

    Function for building charts of fourier processed data and save it
    """

    png_file_name = get_png_file_name(file_name, beautiful_name)
    if not need_to_build(png_file_name, f"{PROCESSED}/fft_signal/{png_file_name}", necessary):
        return

    log.info(f"Fourier Transform: Starting build {png_file_name}")

    xf, yf = solve_fourier_transform(file_name)
    xf, yf = (
        np.clip(xf, 0, SAMPLE_RATE // 2 + 1),
        np.clip(yf, 0, 2.5 * 10 ** 7)
    )

    plt.plot(xf, np.abs(yf))

    plt.title(beautiful_name)
    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    plt.ylim(0, 2.5 * 10 ** 7)

    plt.savefig(f"{PROCESSED}/fft_signal/{png_file_name}", transparent=True)
    plt.clf()

    log.info(f"End {file_name}")


if __name__ == '__main__':

    setup_matplotlib_text_color('black')
    setup_matplotlib(**{'font.size': '13'})

    build_charts_from_dir(
        f"{PROCESSED}/json",
        fourier_transform,
        file_names=get_file_data(f"{RAW}/songs_names.json"),

    )
