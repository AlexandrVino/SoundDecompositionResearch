from generate_wave import SAMPLE_RATE, DURATION
from mix_waves import normalized_tone
from matplotlib import pyplot as plt
import numpy as np
from scipy.fft import rfft, rfftfreq

# число точек в normalized_tone
N = SAMPLE_RATE * DURATION

# обратите внимание на r в начале имён функций
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1/SAMPLE_RATE)

if __name__ == '__main__':
    plt.plot(xf, np.abs(yf))
    plt.show()
