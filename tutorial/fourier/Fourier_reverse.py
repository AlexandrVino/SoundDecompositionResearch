from scipy.fft import irfft
from Fourier_filter_tone import yf
from matplotlib import pyplot as plt
from save_wave import save_wave
from generate_wave import SAMPLE_RATE

new_sig = irfft(yf)

if __name__ == '__main__':
    plt.plot(new_sig[:1000])
    plt.show()
    # save_wave('absolute normalize tone', SAMPLE_RATE, new_sig)
