from scipy.fft import fft, fftfreq
from load import get_file_data
import logging
import matplotlib.pyplot as plt
from utils.my_argparse import setup_basic_config
import numpy as np
import os

args = setup_basic_config()
log = logging.getLogger(__name__)


def fourier_transform(filename):
    """
    :param filename
    :return: None

    Function for build charts of fourier processed data and save it
    """
    log.info(f"Get data {filename}")
    normalized_tone = get_file_data(filename)

    # число точек
    n = len(normalized_tone)
    # частота дискретизации
    sample_rate = 44100

    log.info(f"Build axes {filename}")
    yf = fft(normalized_tone)
    xf = fftfreq(n, 1 / sample_rate)

    log.info(f"Build chart {filename}")
    plt.plot(xf, np.abs(yf))
    plt.title(filename)

    if f"{filename}.jpg" not in os.listdir("../source/processed/fft_signal"):
        log.info(f"Save chart {filename}")
        plt.savefig(f"../source/processed/fft_signal/{filename.split('.')[0]}")

    # plt.show()
    plt.clf()

    log.info(f"End {filename}")


for filename in os.listdir("../source/processed/json"):
    if not filename.endswith('.py'):
        fourier_transform(filename)
