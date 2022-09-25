import os
from argparse import ArgumentTypeError, Namespace
from typing import Callable
from aiomisc.log import basic_config, LogFormat
from configargparse import ArgumentDefaultsHelpFormatter, ArgumentParser

ENV_VAR_PREFIX = 'sound_decomposition_'

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    formatter_class=ArgumentDefaultsHelpFormatter
)

# logging group
parser.add_argument(
    '--input-from', required=False, help='file (dir) name to upload (the script will find it by itself)', default='mp3'
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


def setup_basic_config() -> Namespace:
    args = parser.parse_args()
    clear_environ(lambda arg: arg.startswith(ENV_VAR_PREFIX))
    basic_config(args.log_level, args.log_format, buffered=True)
    return args


def validate(arg_type: Callable, constrain: Callable) -> Callable:
    """
    :param arg_type: type for that must convert value
    :param constrain:
    :return: Filter function

    Function that create filters
    (For example: positive_int = validate(int, constrain=lambda x: x > 0))
    """

    def wrapper(value):
        value = arg_type(value)
        if not constrain(value):
            raise ArgumentTypeError
        return value

    return wrapper


def clear_environ(rule: Callable):
    """
    :param rule: the rule for clean .env variables
    :return:

    Function that clears environment variables, the variables to be cleaned are determined by the passed
    the rule function.
    """

    # Ключи из os.environ копируются в новый tuple, чтобы не менять объект
    # os.environ во время итерации.
    for name in filter(rule, tuple(os.environ)):
        os.environ.pop(name)
