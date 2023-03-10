import json

import numpy as np
from matplotlib import pyplot as plt

from __config__ import PROCESSED
from utils.charts.compare_charts import find_song_names
from utils.charts.config import COLORS, NAMES
from scipy import integrate


def plot_average_integrals():
    plt.clf()

    average = list(map(lambda x: (x[0], sorted(x[1])), find_song_names().items()))
    data = [
        [
            round(sum(item_data) / len(item_data), 5),
            NAMES[genre],
            COLORS[genre]
        ] for genre, item_data in average
    ]

    items_data = np.array(data)
    fig, ax = plt.subplots()

    for (data, name, color) in items_data:
        ax.bar([name], [float(data)], color=color)

    # ax.tick_params(color='white', labelcolor='white')
    # for spine in ax.spines.values():
    #     spine.set_edgecolor('white')

    ax.set_ylabel('Значение Интегралов')
    # ax.legend()

    plt.ylim(0, max(np.array(items_data[:, 0], dtype=np.float)) * 1.3)
    plt.savefig(f"{PROCESSED}/least_squares/integrals.png", transparent=True)
    plt.show()
