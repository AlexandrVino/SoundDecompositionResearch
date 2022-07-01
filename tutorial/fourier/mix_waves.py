import numpy as np
from matplotlib import pyplot as plt
from generate_wave import generate_sine_wave, SAMPLE_RATE, DURATION
from save_wave import save_wave

_, nice_tone = generate_sine_wave(400, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(4000, SAMPLE_RATE, DURATION)

noise_tone = noise_tone * 0.3
mixed_tone = nice_tone + noise_tone

normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

if __name__ == '__main__':
    plt.plot(noise_tone[:1000])
    plt.title('noise tone')
    plt.show()
    # save_wave('noise_tone', SAMPLE_RATE, noise_tone)

    plt.plot(nice_tone[:1000])
    plt.title('nice tone')
    plt.show()
    # save_wave('nice_tone', SAMPLE_RATE, nice_tone)

    plt.plot(normalized_tone[:1000])
    plt.title('normalize tone')
    plt.show()
    # save_wave('normalize tone', SAMPLE_RATE, normalized_tone)
