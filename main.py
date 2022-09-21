import os

from __config__ import PROJECT_SOURCE_RAW
from utils.argparse import clear_environ
from utils.load import check_dir, check_file, load_middleware
from utils.write import save_middleware
from aiomisc.log import basic_config, LogFormat

from configargparse import ArgumentDefaultsHelpFormatter, ArgumentParser

ENV_VAR_PREFIX = 'sound_decomposition_'

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    formatter_class=ArgumentDefaultsHelpFormatter
)

# logging group
parser.add_argument(
    '--input-from', required=True, help='file (dir) name to upload (the script will find it by itself)', default='mp3'
)
parser.add_argument(
    '--output-file', default=None
)

# logging group
parser.add_argument(
    '--log-level', default='info',
    choices=('debug', 'info', 'warning', 'error', 'fatal')
)
parser.add_argument(
    '--log-format', default='color',
    choices=LogFormat.choices()
)


def main():
    """
    :return: None

    Main function
    """

    args = parser.parse_args()
    clear_environ(lambda arg: arg.startswith(ENV_VAR_PREFIX))
    basic_config(args.log_level, args.log_format, buffered=True)

    input_file = args.input_from

    if '.' in input_file:
        check_file(input_file)
    else:
        check_dir(f'{PROJECT_SOURCE_RAW}/{input_file}/')

    # Don't print this because it's pass a lot of time to write data in console
    # print(array_of_samples)


if __name__ == '__main__':
    main()
