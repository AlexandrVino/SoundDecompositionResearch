import json
from typing import Any, List

from scipy.io import wavfile

from config import PROJECT_SOURCE_PROCESSED, PROJECT_SOURCE_RAW


def prepare_to_load(obj: str | List[Any]) -> list | Any:
    """
    :param obj: Iterable obj
    :return: data as List obj to write in json

    Function, convert string values to int
    (The json format doesn't support int16, so it is written as str)
    """

    if isinstance(obj, List):
        return list(map(lambda x: prepare_to_load(x), obj))
    return int(obj)


def load_wav(absolute_path: str) -> List[Any]:
    """
    :param absolute_path: Absolute path for input file
    :return: Array of input file data

    Function, that loads *.wav files
    """

    samplerate, data = wavfile.read(absolute_path)
    return data


def load_mp3(absolute_path: str) -> List[Any]:
    """
    :param absolute_path: Absolute path for input file
    :return: Array of input file data

    Function, that loads *.mp3 files
    """

    pass


def load_txt(absolute_path: str) -> List[Any]:
    """
    :param absolute_path: Absolute path for input file
    :return: Array of input file data

    Function, that loads *.txt files
    """

    with open(absolute_path, 'r', encoding='utf8') as input_file:
        return prepare_to_load(json.load(input_file))


def load_json(absolute_path: str) -> List[Any]:
    """
    :param absolute_path: Absolute path for input file
    :return: Array of input file data

    Function, that loads *.txt files
    """

    with open(absolute_path, 'r', encoding='utf8') as input_file:
        return prepare_to_load(json.load(input_file))


def load_middleware(load_type: str, file_name: str) -> List[int]:
    """
    :param load_type: Loading data from raw or processed files
    :param file_name: relative file path
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    read_func: dict = {
        'raw': [
            PROJECT_SOURCE_RAW,
            {
                'wav': load_wav,
                'mp3': load_mp3
            }
        ],

        'processed': [
            PROJECT_SOURCE_PROCESSED,
            {
                'json': load_json,
                'txt': load_txt,
            }
        ]
    }

    root, load_type_func = read_func.get(load_type, ('', {}))
    file_type: str = file_name.split('.')[-1]
    absolute_path: str = f'{root}\\{file_type}\\{file_name}'

    if not load_type_func:
        raise ValueError(
            f'Unknown load type "{load_type}" '
            f'(load types must be one of ({", ".join(key for key in read_func.keys())})'
        )

    func = load_type_func.get(file_type)
    if not func:
        raise ValueError(
            f'Unknown file type "{file_type}" '
            f'(file types must be one of ({", ".join(f".{key}" for key in load_type_func.keys())})'
        )

    return func(absolute_path)
