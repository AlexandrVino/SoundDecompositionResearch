import matplotlib.pyplot as pylab
import numpy
import pywt
import scipy.io.wavfile as wavfile
from math import log2


# Найти наибольшую мощность двух каналов, которая меньше или равна входу.
def lepow2(x):
    return int(2 ** float(log2(x)))


# Скалограмма с учетом дерева MRA.
def scalogram(data):
    bottom = 0
    vmin = min(map(lambda x: min(abs(x)), data))
    vmax = max(map(lambda x: max(abs(x)), data))
    pylab.gca().set_autoscale_on(False)
    for row in range(0, len(data)):
        scale = 2.0 ** (row - len(data))
        pylab.imshow(
            numpy.array([abs(data[row])]),
            interpolation='nearest',
            vmin=vmin,
            vmax=vmax,
            extent=[0, 1, bottom, bottom + scale])
        bottom += scale


# Загрузите сигнал, возьмите первый канал.
rate, signal = wavfile.read('../../source/raw/wav/websdr.wav')
signal = signal[0:lepow2(len(signal))]
tree = pywt.wavedec(signal, 'coif5')
pylab.gray()
scalogram(tree)
pylab.show()
