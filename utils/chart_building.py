from load import get_file_data
import matplotlib.pyplot as plt
import logging

from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def build_chart(filename):
    """
    :param filename: local path to filename
    :return chart: input signal per beat


    """

    log.info(f"get data {filename}")
    data = get_file_data(filename)
    log.info(f"build chart {filename}")
    plt.plot([abs(val) for val in data])
    plt.title(filename)
    plt.show()


build_chart("shashlindos.json")
build_chart("Vivaldi_metal_cover.json")
build_chart("paparazzi.json")