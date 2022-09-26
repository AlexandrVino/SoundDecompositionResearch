import os

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

    Function for building charts of input signal and save it
    """
    log.info(f"Get data {filename}")
    data = get_file_data(filename)
    log.info(f"Build chart {filename}")
    plt.plot([abs(val) for val in data])
    plt.title(filename)

    if f"{filename}.jpg" not in os.listdir("../source/processed/input_signal"):
        log.info(f"Save chart {filename}")
        plt.savefig(f"../source/processed/input_signal/{filename.split('.')[0]}")

    log.info(f"Show chart {filename}")
    plt.show()
    plt.clf()
    log.info(f"End {filename}")


for filename in os.listdir("../source/processed/json"):
    if not filename.endswith('.py'):
        build_chart(filename)

