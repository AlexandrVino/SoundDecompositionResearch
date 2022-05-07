import librosa
import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import rfft, rfftfreq


SAMPLE_RATE = 22000  # Гц
DURATION = 5  # Секунды


def generate_sine_wave(freq, sample_rate, duration):
    # freq - частота
    x = np.linspace(0, duration, sample_rate*duration, endpoint=False)
    frequencies = x * freq
    # 2pi для преобразования в радианы
    y = np.sin((2 * np.pi) * frequencies)
    return x, y


def get_tone():
    audio_data = 'shashlindos.wav'
    x, sr = librosa.load(audio_data)
    return x


if __name__ == '__main__':
    x = get_tone()
    plt.plot(x)
    plt.show()

    # число точек в tone
    N = SAMPLE_RATE * DURATION

    # обратите внимание на r в начале имён функций
    yf = rfft(x)
    xf = rfftfreq(N, 1 / SAMPLE_RATE)

    plt.plot(xf, np.abs(yf))
    plt.show()
