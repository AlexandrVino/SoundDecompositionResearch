import logging
import os

from __config__ import PROCESSED, RAW
from utils.files.write import save_middleware
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)


def update_config():
    songs_data = {}

    def _wrapper(title, write=False, **kwargs):
        songs_data[title] = songs_data.get(title, {}) | kwargs
        if write:
            save_middleware(songs_data, 'json', f'songs_data.json')

    return _wrapper


def rename_files(dir_name, sep='\t'):
    for file_name in os.listdir(dir_name):

        if os.path.isdir(f"{dir_name}/{file_name}"):
            rename_files(f"{dir_name}/{file_name}", sep=sep + '\t')
        else:
            input_file_name = f"{dir_name}/{file_name}"
            *output_file_name, frmt = input_file_name.split('.')
            output_file_name = '_'.join(output_file_name) + '.' + frmt
            log.info(input_file_name + '\t' + output_file_name)
            os.rename(input_file_name, output_file_name)


