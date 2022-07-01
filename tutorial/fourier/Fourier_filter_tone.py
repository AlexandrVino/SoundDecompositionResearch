from generate_wave import SAMPLE_RATE
from Fourier_RFFT import yf, xf
import numpy as np
from matplotlib import pyplot as plt

# Максимальная частота составляет половину частоты дискретизации
points_per_freq = len(xf) / (SAMPLE_RATE / 2)

# Наша целевая частота - 4000 Гц
target_idx = int(points_per_freq * 4000)

# Обнулим yf для индексов около целевой частоты:
yf[target_idx-2:target_idx+2] = 0

if __name__ == '__main__':
    plt.plot(xf, np.abs(yf))
    plt.show()
