from __config__ import PROCESSED, RAW
from utils.files.load import read_file, read_files_from_dir
from utils.my_argparse import setup_basic_config


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
        root = RAW if input_file in ('mp3', 'wav') else PROCESSED
        read_files_from_dir(f'{root}/{input_file}/')

    # Don't print this because it's pass a lot of time to write data in console
    # print(array_of_samples)


if __name__ == '__main__':
    main()
