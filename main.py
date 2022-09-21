from utils.argparse import clear_environ
from utils.load import load_middleware
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
    '--input-file', required=True
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

    data = load_middleware('raw', args.input_file)
    array_of_samples = data.get_array_of_samples()

    save_middleware(array_of_samples, 'json')
    save_middleware(array_of_samples, 'txt')

    # Don't print this because it's pass a lot of time to write data in console
    # print(array_of_samples)


if __name__ == '__main__':
    main()
