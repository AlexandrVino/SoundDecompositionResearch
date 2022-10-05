from scipy.fft import fft, fftfreq

from __config__ import PROJECT_SOURCE_PATH, PROJECT_SOURCE_PROCESSED
from load import get_file_data
import logging
import matplotlib.pyplot as plt

from utils.chart_building import build_charts_from_dir
from utils.my_argparse import setup_basic_config
import numpy as np
import os

args = setup_basic_config()
log = logging.getLogger(__name__)


def fourier_transform(file_name: str):
    """
    :param file_name
    :return: None

    Function for building charts of fourier processed data and save it
    """

    log.info(f"Fourier Transform")
    log.info(f"Get data {file_name}")
    normalized_tone = get_file_data(file_name)

    # число точек
    n = len(normalized_tone)
    # частота дискретизации
    sample_rate = 44100

    log.info(f"Build axes {file_name}")
    yf = fft(normalized_tone)
    xf = fftfreq(n, 1 / sample_rate)

    log.info(f"Build chart {file_name}")
    plt.plot(xf, np.abs(yf))

    # Setup limit to view on y (from 0 to 2 * 10^8)
    plt.ylim([0, 0.2 * 10**9])

    plt.title(file_name)

    if f"{file_name}.jpg" not in os.listdir(f"{PROJECT_SOURCE_PROCESSED}/fft_signal"):
        log.info(f"Save chart {file_name}")
        plt.savefig(f"{PROJECT_SOURCE_PROCESSED}/fft_signal/{file_name.split('.')[0].split('/')[-1]}")

    plt.clf()

    log.info(f"End {file_name}")


if __name__ == '__main__':
    build_charts_from_dir(f"{PROJECT_SOURCE_PROCESSED}/json", fourier_transform)
