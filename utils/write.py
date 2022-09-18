import json
import os

from typing import Iterable, List

from config import PROJECT_SOURCE_PROCESSED


def prepare_to_write(obj: Iterable | int) -> List | str:
    """
    :param obj: Iterable obj
    :return: data as List obj to write in json

    Function, convert different iterable types to json serializable
    """
    print(obj)
    if isinstance(obj, Iterable):
        return list(map(lambda x: prepare_to_write(x) if isinstance(x, Iterable) else str(x), obj))
    return str(obj)


def write_data_json(data: Iterable, absolute_path: str = None) -> None:
    """
    :param data: Iterable obj
    :param absolute_path: relative path to the file to write data
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    with open(absolute_path, 'w') as write_file:
        json.dump(prepare_to_write(data), write_file, ensure_ascii=False)


def write_data_txt(data: Iterable, absolute_path: str = None) -> None:
    """
    :param data: Iterable obj
    :param absolute_path: relative path to the file to write data
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    with open(absolute_path, 'w') as write_file:
        write_file.write(json.dumps(prepare_to_write(data), ensure_ascii=False))


def save_middleware(data: Iterable, file_type: str, file_name: str = None):
    """
    :param data: data to write
    :param file_name: relative file path
    :param file_type: relative file path
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    write_func: dict = {
        'json': write_data_json,
        'txt': write_data_txt,
    }

    if not file_name:
        file_name = f'file_%i.{file_type}' % len(os.listdir(f'{PROJECT_SOURCE_PROCESSED}/{file_type}/'))

    absolute_path: str = f'{PROJECT_SOURCE_PROCESSED}\\{file_type}\\{file_name}'

    func = write_func.get(file_type)
    if not func:
        raise ValueError(
            f'Unknown file type "{file_type}" '
            f'(file types must be one of ({", ".join(f".{key}" for key in write_func.keys())})'
        )
    func(data, absolute_path)
