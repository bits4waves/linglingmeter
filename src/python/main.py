import librosa

VIOLIN_MIN_F=librosa.note_to_hz('G3')
VIOLIN_MAX_F=librosa.note_to_hz('E7')
# Approximately 0.9715319411536059
FIFTY_CENTS_BWD = pow(2, -50/1200)
# Approximately 1.029302236643492
FIFTY_CENTS_FWD = pow(2, 50/1200)


def get_pitch_series(snd_filename, fmin=VIOLIN_MIN_F,
                     fmax=VIOLIN_MAX_F):
    """Extract f0 history from sound file."""
    y, sr = librosa.load(snd_filename)
    f0, voiced_flag, voiced_probs = \
        librosa.pyin(y, fmin=VIOLIN_MIN_F, fmax=VIOLIN_MAX_F)

    return y, f0


def integrate_partials(frequencies, spectrum):
    """Sum the intensities of the peaks in a sound spectrum.

    This function integrates the peaks corresponding to the partials.

    ‘spectrum’ is an array with sound the sound intensities (dB)
    for each frequency (Hz) in ‘frequencies’.


    Example:

    Suppose we have a sound sample containing:
    220 Hz as the fundamental (1st partial), along with the first 2
    upper partials, 2 * 220 = 440 Hz, and 3 * 220 = 660 Hz.

    In this case, we could have the following arrays for ‘spectrum’
    and ‘frequencies’:

    |  i | frequencies | spectrum |
    |----+-------------+-------------|
    |  0 |          50 | -80         |
    |  1 |         100 |             |
    |  2 |         150 |             |
    |  3 |         200 | x           |
    |  4 |         250 |             |
    |  5 |         300 |             |
    |  6 |         350 |             |
    |  7 |         400 |             |
    |  8 |         450 | x           |
    |  9 |         500 |             |
    | 10 |         550 |             |
    | 11 |         600 |             |
    | 12 |         650 |             |
    | 13 |         700 |             |
    | 14 |         750 |             |
    | 15 |         800 |             |

    | partial | frequency | min_x | max_x |
    |---------+-----------+-------+-------|
    |       1 |       220 |   214 |   226 |
    |       2 |       440 |   427 |   453 |
    |       3 |       660 |   641 |   679 |

    encontra f0

    i = 0
    partial = 1
    integral = 0
    enquanto i < len(frequencias):
        pico_atual = f0 * partial

        x_min = deduz_50_cents(pico_atual)
        x_max = adiciona_50_cents(pico_atual)

        enquanto frequencias[i] < x_min:
            i += 1

        enquanto frequencias[i] < x_max:
            integral += espectro[i]
            i += 1

        partial += 1
    """


y, pitch = get_pitch_series('/home/rafa/sci/sound/440-02-partials/440-02-partials.wav')

# Overlay F0 over a spectrogram

import matplotlib.pyplot as plt
import numpy as np
import librosa.display

amplitude = np.abs(librosa.stft(y))
dB = librosa.amplitude_to_db(amplitude, ref=np.max)

fig, ax = plt.subplots()
img = librosa.display.specshow(dB, x_axis='time', y_axis='log', ax=ax)
ax.set(title='pYIN fundamental frequency estimation')
fig.colorbar(img, ax=ax, format="%+2.f dB")
times = librosa.times_like(pitch)
ax.plot(times, pitch*FIFTY_CENTS_BWD, label='bwd', color='red', linewidth=1)
ax.plot(times, pitch, label='f0', color='cyan', linewidth=1)
ax.plot(times, pitch*FIFTY_CENTS_FWD, label='fwd', color='red', linewidth=1)
ax.legend(loc='upper right')
fig.savefig('plot.png')

# for each entry in the array
# find peaks
# extract pitch

# for i = 1, 2, …, len(peaks)
#     partial = pitch * i
#     for peak in peaks
#         if abs((partial - peak) / partial) ≤ threshold
#             integral_peaks += integrate_peak(peak)

# score = integral_peaks / integrate_tail(pitch)
