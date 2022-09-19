from utils.load import load_middleware
from utils.write import save_middleware


def main():
    data = load_middleware('raw', 'shashlindos.mp3')
    save_middleware(data, 'json')
    save_middleware(data, 'txt')
    pass


if __name__ == '__main__':
    main()
