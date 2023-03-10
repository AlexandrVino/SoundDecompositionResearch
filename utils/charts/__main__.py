import logging
import os
from typing import Callable

from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def build_charts_from_dir(dir_name: str, func: Callable, sep='', file_names=None) -> None:
    """
    :param sep: sep
    :param dir_name: dir from we should plot charts
    :param func: Callable object (same as function), which we use to plot
    :param file_names: Dict with beautiful names of the files
    :return:
    """

    if file_names is None:
        file_names = {}

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


def need_to_build(filename: str, path: str, necessary: list = None) -> bool:
    """
    :param filename:
    :param path:
    :param necessary:
    :return:
    """

    if necessary is None:  # start selection
        necessary = ['wewillrockyou', 'nothingelsematters', 'бетховен-луннаясоната', 'dabro-юность']

    if os.path.exists(path):
        log.info(f"{filename} already exists")
        return False

    if not any(need.lower() in filename.split('/')[-1].lower().replace(' ', '') for need in necessary):
        log.info(f"{filename} is not necessary")
        return False

    return True


def get_png_file_name(file_name: str, beautiful_name: str = '') -> str:
    """
    :param file_name:
    :param beautiful_name:
    :return:
    """

    return (
        '/'.join([file_name.split('.')[0].split('/')[-2], beautiful_name]) if beautiful_name
        else '/'.join(''.join(file_name.split('.')[:-1]).split('/')[-2::])
    )
