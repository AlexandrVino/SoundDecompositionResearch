import os
from typing import Callable

from __config__ import SOURCE_PATH, PROCESSED, RAW
from utils.load import get_file_data, read_file
import matplotlib.pyplot as plt
import logging

from utils.matplotlibSetup import setup_matplotlib_font, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def build_chart(file_name: str, beautiful_name: str = '') -> None:
    """
    :param file_name: local path to filename
    :param beautiful_name: Beautiful name of the file
    :return chart: input signal per beat

    Function for building charts of input signal and save it
    """

    png_file_name = '/'.join([file_name.split('.')[0].split('/')[-2], beautiful_name]) \
        if beautiful_name else '/'.join(file_name.split('.')[0].split('/')[-2::])

    if os.path.exists(f"{PROCESSED}/input_signal/{png_file_name}.png"):
        return

    need = ['wewillrockyou', 'Nothingelsematters', 'dabro', 'Луннаясоната', ]
    if not any(n.lower() in png_file_name.lower().replace(' ', '') for n in need):
        return

    log.info(f"Get data {file_name}")
    data = get_file_data(file_name)

    log.info(f"Build chart {file_name}")
    plt.plot([abs(val) / 1000 for val in data])

    plt.ylabel('Амплитуда')
    plt.xlabel('Время')
    plt.title(beautiful_name)

    log.info(f"Save chart {file_name}")
    plt.savefig(f"{PROCESSED}/input_signal/{png_file_name}", transparent=True)

    log.info(f"Show chart {file_name}")
    plt.show()
    plt.clf()
    log.info(f"End {file_name}")


def build_charts_from_dir(dir_name: str, func: Callable, sep='', file_names: dict = {}) -> None:
    """

    :param sep: sep
    :param dir_name: dir from we should plot charts
    :param func: Callable object (same as function), which we use to plot
    :param file_names: Dict with beautiful names of the files
    :return:
    """

    log.info(f"{sep}{dir_name}")

    for file_name in os.listdir(dir_name):

        if os.path.isdir(f"{dir_name}/{file_name}"):
            build_charts_from_dir(f"{dir_name}/{file_name}", func, sep=sep + '\t', file_names=file_names)
        else:
            log.info(sep + '\t' + file_name)
            if not file_name.endswith('.py') and not file_name.endswith('.png'):
                func(f"{dir_name}/{file_name}", file_names.get(file_name.split('.')[0], file_name.split('.')[0]))

        log.info(f"{sep}\tFINISHED\t" + file_name)
    log.info("FINISHED")


if __name__ == '__main__':
    setup_matplotlib_text_color('white')
    setup_matplotlib_font(**{'font.size': '13'})
    build_charts_from_dir(
        f"{PROCESSED}/json",
        build_chart,
        file_names=get_file_data(f"{RAW}/songs_names.json")
    )
