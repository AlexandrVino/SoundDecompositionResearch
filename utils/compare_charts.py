import json
import logging
import os

import matplotlib.pyplot as plt
import numpy as np

from __config__ import PROCESSED, RAW
from utils.load import get_file_data
from utils.LPSpace import solve_one_integral
from utils.matplotlibSetup import setup_matplotlib, setup_matplotlib_text_color
from utils.my_argparse import setup_basic_config

args = setup_basic_config()
log = logging.getLogger(__name__)

setup_matplotlib_text_color('black')
setup_matplotlib(**{'font.size': '13'})

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

songs_data = get_file_data(f"{PROCESSED}/songs_data.json")


def f(x: int, a: list[int]) -> int:
    return round(a[0] * x ** 2 + a[1] * x + a[2])


def find_song_names(directory='all'):
    """
    :param directory: all / each / directory_name
    """
    songs_names = get_file_data(f"{RAW}/songs_names.json")
    data = list()

    dir_name = f"{PROCESSED}/json"
    for dir in os.listdir(dir_name):
        if dir.endswith('.py'):
            continue

        for file in os.listdir(dir_name + '/' + dir):
            if file.split('.')[0] in songs_names:
                name = songs_names[file.split('.')[0]]
            else:
                name = '/'.join(file.split('.')[0].split('/')[-2::])

            if file.endswith('.py'):
                continue
            elif directory == 'each':
                data.append([file, name, dir])
                break
            elif directory in {dir, 'all'}:
                data.append([file, name, dir])
            else:
                break

    already = []
    average = {}
    integrals = {}

    fig, ax = plt.subplots()
    for elem in data:
        build_one_chart(*elem, ax, already, average, integrals)

    ax.tick_params(color='white', labelcolor='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')
    ax.legend()

    plt.ylabel('Амплитуда')
    plt.xlabel('Частота')
    plt.savefig(f"{PROCESSED}/least_squares/compare_charts.png", transparent=True)
    plt.show()
    return average


def build_one_chart(file_name, beautiful_name, origin, ax, already, average, integrals):
    log.info(f'Build {file_name}')

    if beautiful_name not in songs_data:
        log.info(f'No file data {file_name}')
        return -1
    a = songs_data[beautiful_name]['least_squares']

    kwargs = dict(label=NAMES[origin])
    if kwargs['label'] in already:
        del kwargs['label']
    else:
        already.append(NAMES[origin])

    if not average.get(origin):
        average[origin] = []

    average[origin].append(solve_one_integral(beautiful_name, a)[1])
    integrals[beautiful_name] = average[origin][-1]

    ax.plot([f(x, a) for x in range(25000)], COLORS[origin], **kwargs)


def solution(integrals_solution):
    """
    :param current: current value of integral
    :param title: Title of composition
    :return:
    """

    with open(f'{PROCESSED}/integrals.json') as input_file:
        genres = json.load(input_file)

    with open(f'{PROCESSED}/solution.json', encoding='utf8') as input_file:
        sol = json.load(input_file)

    for title, value in integrals_solution.items():
        solve(genres, sol, value, title)

    with open(f'{PROCESSED}/solution.json', 'w', encoding='utf8') as output_file:
        json.dump(sol, output_file, indent=4, ensure_ascii=False)


def solution_for_oscillation(oscillation_solution):
    """
    :param current: current value of integral
    :param title: Title of composition
    :return:
    """

    with open(f'{PROCESSED}/oscillation.json') as input_file:
        genres = json.load(input_file)

    with open(f'{PROCESSED}/solution.json', encoding='utf8') as input_file:
        sol = json.load(input_file)

    for title, value in oscillation_solution.items():
        solve(genres, sol, value, title)

    with open(f'{PROCESSED}/solution.json', 'w', encoding='utf8') as output_file:
        json.dump(sol, output_file, indent=4, ensure_ascii=False)


def solve(genres, sol, current, title):
    for key, value in genres.items():
        mn, mx = sorted([value, current])
        if not sol.get(title):
            sol[title] = {}
        sol[title][key] = round(mn / mx * 1000, 2)

    sm = sum(sol[title].values())
    for key, value in sol[title].items():
        sol[title][key] = round(value / sm * 100, 2)

    return sol


def plot_average_integrals():
    plt.clf()

    # average = list(map(lambda x: (x[0], sorted(x[1])), find_song_names().items()))
    # data = [
    #     [
    #         round(sum(item_data) / len(item_data), 5),
    #         NAMES[genre],
    #         COLORS[genre]
    #     ] for genre, item_data in average
    # ]
    # print(data)

    data = [[19572370.77467515, 'Классика', '#21dec1'], [81159307.22493343, 'Метал', '#882bc3'],
            [121763891.27453406, 'Поп', '#ff0000'], [84786868.98338048, 'Рок', '#0000fa']]

    items_data = np.array(data)
    fig, ax = plt.subplots()

    for (data, name, color) in items_data:
        ax.bar([name], [float(data)], color=color)

    ax.tick_params(color='black', labelcolor='black')
    for spine in ax.spines.values():
        spine.set_edgecolor('black')

    ax.set_ylabel('Значение колебания')
    # ax.legend()

    plt.ylim(0, max(np.array(items_data[:, 0], dtype=np.float)) * 1.3)
    plt.savefig(f"{PROCESSED}/oscillation/oscillation_avg_ok.png", transparent=True)
    plt.show()


if __name__ == '__main__':
    # integrals_solution = {
    #     'Бетховаен - к Элизе': 272928614201541,
    #     'Бах - Сюита №2': 389878153454718,
    #     'Моцарт - Соната №11': 424011686911891,
    #     'Ludovico Einaudi - Fly': 459766055683055,
    #     'Бетховен - Лунная Соната': 461353478964833,
    #     'Фридерик Шопен - Фантазия-экспромт до-диез-минор, арфа': 675006446778743,
    #     'Петр Ильич Чайковский - Марш Из Балета Щелкунчик': 717631724895771,
    #     'Вивальди - Времена Года (Зима)': 1056041872230682,
    #     'Моцарт - симфония №40': 1063645457001178,
    #     'Mozart - Маленькая Ночная Серенада Аллегро': 1101940939898704,
    #     'Сергей Прокофьев - Танец рыцарей (Балет Ромео и Джульетта, Картина Вторая)': 1104112313961104,
    #     'Антонио Вивальди - Осень': 1203812069092099,
    #     'Петр Ильич Чайковский - Вальс Цветов': 1288538970097158,
    #     'Антонио Вивальди - Лето': 1342654844109467,
    #     'Вагнер - Полет Валькирий': 2098274614457001,
    #     'QUEEN - We Will Rock You': 2411845177981689,
    #     'OPETH - Benighted': 2448954804775267,
    #     'guns-n039-roses-don039t-cry': 2930502838951098,
    #     'No': 3023565473276510, 'europe-carrie': 3064166396956886,
    #     "Guns & Roses - Don't Cry": 3090774888847022,
    #     'skid-row-18-and-life': 3376179902940316,
    #     'linkin-park-in-the-end': 3694514695333535,
    #     'Lady Gaga - Paparazzi': 3837386356316094,
    #     'METALLICA - Nothing Else Matters ': 3888028209256786,
    #     'imagine-dragons-demons': 4050014988609734,
    #     'Lamb Of God - Walk with Me In Hell': 4100970586270982,
    #     'ljapis-trubeckojj-voiny-sveta': 4158809398936860,
    #     'metallica-the-unforgiven': 4359484132835800,
    #     'papa-roach-last-resort': 4369798538977432,
    #     'metallica-enter-sandman': 4403183194356534,
    #     'Акула - Кислотный Диджей': 4579595173959673,
    #     'Паша Сникерс - Не работать это моя работа': 4625425969710236,
    #     'Big Baby Tape, kizaru - Million': 4629265629987491,
    #     'dire-straits-sultans-of-swing': 4636586510470210,
    #     'evanescence-bring-me-to-life': 4644695141877641,
    #     'nickelback-burn-it-to-the-ground': 4669416821741676,
    #     'Порнофильмы - В диапазоне': 4707260142143104,
    #     'metallica-wherever-i-may-roam': 4728057121896791,
    #     'metallica-sad-but-true': 4728435161910524,
    #     'nightwish-she-is-my-sin': 4759808979624309,
    #     'UncleFlexxx - Camry 3': 4779443909721725,
    #     'nervy-samyjj-dorogojj-chelovek': 4807432290491694,
    #     'Bullet for my valentine - Tears Dont Fall': 4839827084822567,
    #     'Иван Дорн - Стыцамэн ': 4867510369428136,
    #     'DABRO - Юность': 4871238068911061,
    #     'numer-482-dobrijj-ranok-ukrayino': 4970051978746617,
    #     'splin-vykhoda-net': 5038241890834722,
    #     'fall-out-boy-centuries': 5056321111051028,
    #     'SCORPIONS - Still Loving You': 5071710086612195,
    #     'Николай Басков - Натуральный блондин': 5108663116294911,
    #     'INSTASAMKA - DADADA': 5252356836798459,
    #     'bi-2-kompromiss': 5394304695055430,
    #     'ЕГОР КРИД - Самая самая': 5480011191373022,
    #     'leningrad-v-pitere-pit': 5698654990063436,
    #     'Хлеб - Шашлындос': 5798134138655503,
    #     'Пуси Джуси - Инстасамка [mp3ten': 6378093715413223,
    #     'GONE': 6378426365804057,
    #     'Юрий Шатунов - Седая Ночь': 6723715587443644,
    #     'twenty-one-pilots-stressed-out': 6896971892489209}
    #
    # solution(integrals_solution)
    plot_average_integrals()
