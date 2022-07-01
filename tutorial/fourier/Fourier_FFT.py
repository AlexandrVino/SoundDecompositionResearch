from scipy.fft import fft, fftfreq
from generate_wave import SAMPLE_RATE, DURATION
from mix_waves import normalized_tone
from matplotlib import pyplot as plt
import numpy as np

# число точек в normalized_tone
N = SAMPLE_RATE * DURATION

yf = fft(normalized_tone)
xf = fftfreq(N, 1 / SAMPLE_RATE)

if __name__ == '__main__':
    plt.plot(xf, np.abs(yf))
    plt.title('частотный спектр сигнала')
    plt.show()
