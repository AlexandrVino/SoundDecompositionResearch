from __config__ import PROCESSED
from utils.files.load import get_file_data

COLORS = {
    'classical_music': '#21dec1',
    'metal': '#882bc3',
    'other': '#ff0000',
    'rock': '#0000fa'
}

NAMES = {
    'classical_music': 'Классика',
    'metal': 'Метал',
    'other': 'Поп',
    'rock': 'Рок'
}

SONGS_DATA = get_file_data(f"{PROCESSED}/songs_data.json")

SAMPLE_RATE = 44100
