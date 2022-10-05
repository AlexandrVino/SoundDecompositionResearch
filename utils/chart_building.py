import os
from typing import Callable

from __config__ import PROJECT_SOURCE_PATH
from load import get_file_data
import matplotlib.pyplot as plt
import logging

from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def build_chart(file_name: str) -> None:
    """
    :param file_name: local path to filename
    :return chart: input signal per beat

    Function for building charts of input signal and save it
    """
    log.info(f"Get data {file_name}")
    data = get_file_data(file_name)
    log.info(f"Build chart {file_name}")
    plt.plot([abs(val) for val in data])
    plt.title(file_name)

    if f"{file_name}.jpg" not in os.listdir("../source/processed/input_signal"):
        log.info(f"Save chart {file_name}")
        plt.savefig(f"../source/processed/input_signal/{file_name.split('.')[0]}")

    log.info(f"Show chart {file_name}")
    plt.show()
    plt.clf()
    log.info(f"End {file_name}")


def build_charts_from_dir(dir_name: str, func: Callable) -> None:

    """

    :param dir_name: dir from we should plot charts
    :param func: Callable object (same as function), which we use to plot
    :return:
    """

    log.info(dir_name)

    for file_name in os.listdir(dir_name):
        if os.path.isdir(f"{dir_name}/{file_name}"):
            build_charts_from_dir(f"{dir_name}/{file_name}", func)
        else:
            if not file_name.endswith('.py') and not file_name.endswith('.png'):
                func(file_name)


if __name__ == '__main__':
    build_charts_from_dir(PROJECT_SOURCE_PATH, build_chart)
