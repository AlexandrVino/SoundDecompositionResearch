from __config__ import PROCESSED
from utils.files.load import get_file_data

COLORS = {
    'blues': '#21dec1',
    'classical': '#ffe20f',
    'country': '#ffe20f',
    'disco': '#ffe20f',
    'hiphop': '#ffe20f',
    'jazz': '#ffe20f',
    'metal': '#882bc3',
    'pop': '#ff0000',
    'reggae': '#ff0000',
    'rock': '#0000fa'
}

NAMES = {
    'blues': 'Блюз',
    'classical': 'Классика',
    'country': 'Кантри',
    'disco': 'Диско',
    'hiphop': 'Хип-Хоп',
    'jazz': 'Джаз',
    'metal': 'Метал',
    'pop': 'Поп',
    'reggae': 'Регги',
    'rock': 'Рок'
}

SONGS_DATA = get_file_data(f"{PROCESSED}/songs_data.json")

SAMPLE_RATE = 44100
