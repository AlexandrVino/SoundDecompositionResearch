from scipy.io.wavfile import write


def save_wave(filename, sample_rate, tone):
    write(filename + '.wav', sample_rate, tone)
