import json
import logging
import os

from typing import Iterable, List

from __config__ import PROJECT_SOURCE_PROCESSED

log = logging.getLogger(__name__)


def prepare_to_write_json(obj: Iterable | int) -> List | str:
    """
    :param obj: Iterable obj
    :return: data as List obj to write in json

    Function, convert different iterable types to json serializable
    """

    if isinstance(obj, Iterable):
        return list(map(lambda x: prepare_to_write_json(x) if isinstance(x, Iterable) else str(x), obj))
    return str(obj)


def prepare_to_write_txt(obj: Iterable | int) -> str:
    """
    :param obj: Iterable obj
    :return: data as List obj to write in json

    Function, convert different iterable types to write data in txt
    """

    if isinstance(obj, Iterable):
        return ', '.join(map(lambda x: prepare_to_write_json(x) if isinstance(x, Iterable) else str(x), obj))
    return str(obj)


def write_data_json(data: Iterable, absolute_path: str = None) -> None:
    """
    :param data: Iterable obj
    :param absolute_path: relative path to the file to write data
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    if os.path.exists(absolute_path):
        return

    log.info(f"Writing %s" % absolute_path)
    with open(absolute_path, 'w') as write_file:
        json.dump(prepare_to_write_json(data), write_file, ensure_ascii=False)
    log.info(f"Wrote successful")


def write_data_txt(data: Iterable, absolute_path: str = None) -> None:
    """
    :param data: Iterable obj
    :param absolute_path: relative path to the file to write data
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    log.info(f"Writing %s" % absolute_path)
    with open(absolute_path, 'w') as write_file:
        write_file.write(prepare_to_write_txt(data))
    log.info(f"Wrote successful")


def save_middleware(data: Iterable, file_type: str, file_name: str = None):
    """
    :param data: data to write
    :param file_name: relative file path
    :param file_type: relative file path
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    log.info(f"Start of writing data")

    write_func: dict = {
        'json': write_data_json,
        'txt': write_data_txt,
    }

    if not file_name:
        file_name = f'file_%i.{file_type}' % len(os.listdir(f'{PROJECT_SOURCE_PROCESSED}\\{file_type}\\'))

    absolute_path: str = f'{PROJECT_SOURCE_PROCESSED}\\{file_type}\\{file_name}'

    func = write_func.get(file_type)
    if not func:
        raise ValueError(
            f'Unknown file type "{file_type}" '
            f'(file types must be one of ({", ".join(f".{key}" for key in write_func.keys())})'
        )

    func(data, absolute_path)
    log.info(f"End of data writing")
