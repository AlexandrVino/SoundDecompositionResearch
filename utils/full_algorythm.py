import json
import logging
import numpy as np
from scipy.fft import fft, fftfreq
from utils.load import get_file_data
from utils.my_argparse import setup_basic_config
from utils.write import prepare_to_write_json

args = setup_basic_config()
log = logging.getLogger(__name__)

genres = {
    "classical_music": "Классика",
    "metal": "Метал",
    "other": "Поп",
    "rock": "Рок"
}


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


def full_algorythm(filename):
    log.info(f"Fourier Transform")
    log.info(f"Get genres_oscillation {filename}")

    normalized_tone = get_file_data(filename).get_array_of_samples()

    n = len(normalized_tone)  # число точек
    sample_rate = 44100  # частота дискретизации

    log.info(f"Build axes {filename}")
    yf = fft(normalized_tone)
    xf = fftfreq(n, 1 / sample_rate)

    step = len(xf) // 20000
    oscillation_list = []
    for x in range(0, len(xf), step):
        mini, maxi = min(yf[x:x + step]), max(yf[x:x + step])
        oscillation_list.append(float(maxi - mini))
    oscillation_avg = sum(oscillation_list) / len(oscillation_list)

    with open("source/processed/oscillation.json", "r", encoding="utf-8") as file:
        genres_oscillation: dict = json.load(file)

    relative_oscillation = list()
    for key, value in genres_oscillation.items():
        mn, mx = sorted([value, oscillation_avg])
        relative_oscillation.append(mn / mx)

    relative_oscillation = list(map(lambda x: x / sum(relative_oscillation) * 100, relative_oscillation))
    relative_oscillation = {key: round(value, 1) for key, value in zip(genres.values(), relative_oscillation)}

    return relative_oscillation
