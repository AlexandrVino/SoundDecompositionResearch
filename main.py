from __config__ import PROJECT_SOURCE_PROCESSED, PROJECT_SOURCE_RAW
from utils.my_argparse import clear_environ, setup_basic_config
from utils.load import read_files_from_dir, read_file


def main():
    """
    :return: None

    Main function
    """

    args = setup_basic_config()
    input_file = args.input_from

    if '.' in input_file:
        read_file(input_file)
    else:
        root = PROJECT_SOURCE_RAW if input_file in ('mp3', 'wav') else PROJECT_SOURCE_PROCESSED
        read_files_from_dir(f'{root}/{input_file}/')

    # Don't print this because it's pass a lot of time to write data in console
    # print(array_of_samples)


if __name__ == '__main__':
    main()
