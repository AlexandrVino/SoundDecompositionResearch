import numpy as np
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100  # Гц
DURATION = 5  # Секунды


def generate_sine_wave(freq, sample_rate, duration):
    # freq - частота
    x = np.linspace(0, duration, sample_rate*duration, endpoint=False)
    frequencies = x * freq
    # 2pi для преобразования в радианы
    y = np.sin((2 * np.pi) * frequencies)
    return x, y


if __name__ == '__main__':
    # Генерируем волну с частотой 2 Гц, которая длится 5 секунд
    x, y = generate_sine_wave(2, SAMPLE_RATE, DURATION)
    plt.plot(x, y)
    plt.show()
