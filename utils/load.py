import json
import logging
import os
from pathlib import Path
from typing import Any, List, Tuple

from pydub import AudioSegment

from __config__ import PROJECT_SOURCE_PROCESSED, PROJECT_SOURCE_RAW
from utils.write import save_middleware

log = logging.getLogger(__name__)

# Setup pydub variables
AudioSegment.converter = f"C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = f"C:\\ffmpeg\\bin\\ffprobe.exe"
AudioSegment.ffmpeg = f"C:\\ffmpeg\\bin\\ffmpeg.exe"


# This doesn't work so unzip ffmpeg form "https://disk.yandex.ru/d/BVNQSeq81lADtA" to C:\\
# AudioSegment.converter = f"{PROJECT_PATH}\\ffmpeg\\bin\\ffmpeg.exe"
# AudioSegment.ffprobe = f"{PROJECT_PATH}\\ffmpeg\\bin\\ffprobe.exe"
# AudioSegment.ffmpeg = f"{PROJECT_PATH}\\ffmpeg\\bin\\ffmpeg.exe"


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

    log.info(f"Loading %s" % absolute_path)
    return AudioSegment.from_wav(absolute_path)


def load_mp3(absolute_path: str) -> List[Any]:
    """
    :param absolute_path: Absolute path for input file
    :return: Array of input file data

    Function, that loads *.mp3 files
    """

    log.info(f"Loading %s" % absolute_path)
    return AudioSegment.from_mp3(absolute_path)


def load_txt(absolute_path: str) -> List[Any]:
    """
    :param absolute_path: Absolute path for input file
    :return: Array of input file data

    Function, that loads *.txt files
    """

    log.info(f"Loading %s" % absolute_path)
    with open(absolute_path, 'r', encoding='utf8') as input_file:
        return prepare_to_load(json.load(input_file))


def load_json(absolute_path: str) -> List[Any]:
    """
    :param absolute_path: Absolute path for input file
    :return: Array of input file data

    Function, that loads *.txt files
    """

    log.info(f"Loading %s" % absolute_path)
    with open(absolute_path, 'r', encoding='utf8') as input_file:
        return prepare_to_load(json.load(input_file))


def load_middleware(file_name: str) -> Tuple[List[int], str] | Tuple[AudioSegment, str]:
    """
    :param file_name: relative file path
    :return: Array of input file data

    Function, that choose upload function according to the file type
    """

    log.info(f"Start of loading data")

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

    file_type: str = file_name.split('.')[-1]

    load_type = 'processed' if file_type in ('json', 'txt') else 'raw'

    root, load_type_func = read_func.get(load_type, ('', {}))
    absolute_path: Path = Path(f'{root}\\{file_type}\\{file_name}')

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

    val = func(absolute_path)
    log.info(f"End of data loading")

    return val, file_name


def read_files_from_dir(dir_name: str):
    for file_name in os.listdir(dir_name):
        if os.path.isfile(f"{dir_name}/{file_name}") and '.py' not in file_name:
            read_file(file_name)


def read_file(input_file: str):

    data, file_name = load_middleware(input_file)

    if '.wav' in file_name or '.mp3' in file_name:
        new_file_name = file_name.split('.')[0]
        array_of_samples = data.get_array_of_samples()
        save_middleware(array_of_samples, 'json', file_name=new_file_name + '.json')
        save_middleware(array_of_samples, 'txt', file_name=file_name + '.txt')
    else:

        print(data)


