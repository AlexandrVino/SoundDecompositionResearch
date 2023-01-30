import logging

import matplotlib.pyplot as plt

from __config__ import PROCESSED, RAW
from utils.charts.main import build_charts_from_dir, get_png_file_name, need_to_build
from utils.files.load import get_file_data
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def default_signal_chart(file_name: str, beautiful_name: str = '', necessary=None) -> None:
    """
    :param file_name: local path to filename
    :param beautiful_name: Beautiful name of the file
    :param necessary: List of names songs necessary to build
    :return chart: input signal per beat

    Function for building charts of input signal and save it
    """

    png_file_name = get_png_file_name(file_name, beautiful_name)
    if not need_to_build(png_file_name, f"{PROCESSED}/input_signal/{png_file_name}", necessary):
        return

    log.info(f"Default signal: Starting build {png_file_name}")

    plt.plot([abs(val) / 1000 for val in get_file_data(file_name)])

    plt.ylabel('Амплитуда')
    plt.xlabel('Время')
    plt.title(beautiful_name)

    plt.savefig(f"{PROCESSED}/input_signal/{png_file_name}", transparent=True)
    plt.clf()

    log.info(f"End {file_name}")


if __name__ == '__main__':
    setup_matplotlib_text_color('black')
    setup_matplotlib(**{'font.size': '13'})
    build_charts_from_dir(
        f"{PROCESSED}/json",
        default_signal_chart,
        file_names=get_file_data(f"{RAW}/songs_names.json")
    )
