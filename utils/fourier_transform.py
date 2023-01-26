from scipy.fft import fft, fftfreq

from __config__ import SOURCE_PATH, PROCESSED, RAW
from load import get_file_data
import logging
import matplotlib.pyplot as plt

from utils.chart_building import build_charts_from_dir
from utils.my_argparse import setup_basic_config
import numpy as np
import os
import matplotlib as mpl

mpl.rcParams['agg.path.chunksize'] = 10000

args = setup_basic_config()
log = logging.getLogger(__name__)


def fourier_transform(file_name: str, beautiful_name: str = ''):
    """
    :param file_name: local path to filename
    :param beautiful_name: Beautiful name of the file
    :return: None

    Function for building charts of fourier processed data and save it
    """

    png_file_name = '/'.join([file_name.split('.')[0].split('/')[-2], beautiful_name]) \
        if beautiful_name else '/'.join(file_name.split('.')[0].split('/')[-2::])

    if os.path.exists(f"{PROCESSED}/fft_signal/{png_file_name}.png"):
        return

    log.info(f"Fourier Transform")
    log.info(f"Get data {file_name}")

    normalized_tone = get_file_data(file_name)

    n = len(normalized_tone)  # число точек
    sample_rate = 44100  # частота дискретизации

    log.info(f"Build axes {file_name}")
    yf = fft(normalized_tone)
    xf = fftfreq(n, 1 / sample_rate)

    log.info(f"Build chart {file_name}")
    # plt.plot(np.clip(xf, 0, sample_rate // 2 + 1), np.clip(np.abs(yf), 0, 2.5 * 10 ** 7))
    plt.plot(np.clip(xf, 0, sample_rate // 2 + 1), np.abs(yf))

    plt.title(beautiful_name)
    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')

    log.info(f"Save chart {file_name}")
    plt.savefig(f"{PROCESSED}/fft_signal/{png_file_name}")

    plt.show()
    plt.clf()

    log.info(f"End {file_name}")


if __name__ == '__main__':

    build_charts_from_dir(
        f"{PROCESSED}/json",
        fourier_transform,
        file_names=get_file_data(f"{RAW}/songs_names.json")
    )
