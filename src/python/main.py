import librosa

VIOLIN_MIN_F=librosa.note_to_hz('G3')
VIOLIN_MAX_F=librosa.note_to_hz('E7')
# Approximately 0.9715319411536059
FIFTY_CENTS_BWD = pow(2, -50/1200)
# Approximately 1.029302236643492
FIFTY_CENTS_FWD = pow(2, 50/1200)


def get_f0_series(snd_filename, fmin=VIOLIN_MIN_F,
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
    440 Hz as the fundamental (1st partial), along with the first 2
    upper partials, 2 * 440 = 880 Hz, and 3 * 440 = 1320 Hz.

    For each partial, we determine the intervals to integrate.
    In this example, the threshold is more or less 50 cents
    (see https://en.wikipedia.org/wiki/Cent_(music)).

    We use the proper formula to calculate it:

    FIFTY_CENTS_BELOW = pow(2, -50/1200)
    FIFTY_CENTS_ABOVE = pow(2, 50/1200)

    For instance, for 440 Hz:

    min_x = 440 * FIFTY_CENTS_BELOW
    max_x = 440 * FIFTY_CENTS_ABOVE

    This is shown in the table below.

    | partial | frequency | min_x | max_x |
    |---------+-----------+-------+-------|
    |       1 |       440 |   427 |   453 |
    |       2 |       880 |   855 |   906 |
    |       3 |      1320 |  1282 |  1359 |

    In this case, we could have the following arrays for
    ‘frequencies’ and  ‘spectrum’ shown in the table below.  The
    ‘X’’s in the last column mark the values that fall inside the
    interval we want to integrate.

    |   i | frequencies | spectrum | min_x <= x <= max_x |
    |-----+-------------+----------+---------------------|
    |   0 |           0 |      -80 | -                   |
    |   1 |          11 |      -80 | -                   |
    |   2 |          22 |      -80 | -                   |
    | ... |         ... |      ... | ...                 |
    |  38 |         409 |      -44 | -                   |
    |  37 |         398 |      -52 | -                   |
    |  40 |         431 |       -4 | X                   |
    |  41 |         441 |        0 | X                   |
    |  42 |         452 |       -8 | X                   |
    |  43 |         463 |      -35 | -                   |
    |  44 |         474 |      -47 | -                   |
    | ... |         ... |      ... | ...                 |
    |  78 |         840 |      -51 | -                   |
    |  79 |         851 |      -42 | -                   |
    |  80 |         861 |      -28 | X                   |
    |  81 |         872 |       -8 | X                   |
    |  82 |         883 |       -5 | X                   |
    |  83 |         894 |      -15 | X                   |
    |  84 |         904 |      -36 | X                   |
    |  85 |         915 |      -47 | -                   |
    |  86 |         926 |      -54 | -                   |
    | ... |         ... |      ... | ...                 |
    | 118 |        1270 |      -59 | -                   |
    | 119 |        1281 |      -52 | -                   |
    | 120 |        1292 |      -43 | X                   |
    | 121 |        1303 |      -28 | X                   |
    | 122 |        1314 |      -11 | X                   |
    | 123 |        1324 |      -10 | X                   |
    | 124 |        1335 |      -22 | X                   |
    | 125 |        1346 |      -41 | X                   |
    | 126 |        1357 |      -51 | X                   |
    | 127 |        1367 |      -58 | -                   |
    | 128 |        1378 |      -63 | -                   |
    """
    """
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
    # i should be able to do with f0 and integration_limits
    thing = {'f0': 440,
             'integration_limits': (427, 453),
             'array_indexes': [40, 41, 42],
             'frequencies': [431, 441, 452],
             'spectrum': [-4, 0, -8],
             'integral': None}
    pass


y, f0 = get_f0_series('/home/rafa/dev/sound/440-10-partials/440-10-partials.wav')

# Overlay F0 over a spectrogram

import matplotlib.pyplot as plt
import numpy as np
import librosa.display

amplitude = np.abs(librosa.stft(y))
spectrum = librosa.amplitude_to_db(amplitude, ref=np.max)
frequencies = librosa.fft_frequencies()

fig, ax = plt.subplots()
img = librosa.display.specshow(spectrum, x_axis='time', y_axis='log', ax=ax)
ax.set(title='pYIN fundamental frequency estimation')
fig.colorbar(img, ax=ax, format="%+2.f dB")
times = librosa.times_like(f0)
ax.plot(times, f0*FIFTY_CENTS_BWD, label='bwd', color='red', linewidth=1)
ax.plot(times, f0, label='f0', color='cyan', linewidth=1)
ax.plot(times, f0*FIFTY_CENTS_FWD, label='fwd', color='red', linewidth=1)
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
