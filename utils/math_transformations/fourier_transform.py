import logging

import numpy as np
from scipy.fft import fft, fftfreq

from utils.charts.config import SAMPLE_RATE
from utils.files.load import get_file_data
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def solve_fourier_transform(file_name):
    normalized_tone = get_file_data(file_name)

    return (
        np.clip(fftfreq(len(normalized_tone), 1 / SAMPLE_RATE), 0, SAMPLE_RATE // 2 + 1),
        np.clip(np.abs(fft(normalized_tone)), 0, 2.5 * 10 ** 7)
    )
