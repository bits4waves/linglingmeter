import librosa
import numpy as np
import math

VIOLIN_MIN_F=librosa.note_to_hz('G3')
VIOLIN_MAX_F=librosa.note_to_hz('E7')
# Amount of cents before and after peak frequency to include in the
# integration interval.
THRESHOLD_CENTS=50
TOP_DB=80

def get_f0_series(snd_filename, fmin=VIOLIN_MIN_F,
                  fmax=VIOLIN_MAX_F):
    """Extract f0 history from sound file."""
    y, sr = librosa.load(snd_filename)
    f0, voiced_flag, voiced_probs = \
        librosa.pyin(y, fmin=VIOLIN_MIN_F, fmax=VIOLIN_MAX_F)

    return y, f0


def create_threshold(partial, cents=THRESHOLD_CENTS):
    """Return min and max integration limits."""
    return (partial * pow(2, -cents/1200),
            partial * pow(2, cents/1200))


def integrate_peaks(f0, frequencies, spectrum, cents=THRESHOLD_CENTS):
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
    |   0 |           0 |        0 | -                   |
    |   1 |          11 |        0 | -                   |
    |   2 |          22 |        0 | -                   |
    | ... |         ... |   ...    | ...                 |
    |  38 |         409 |       36 | -                   |
    |  37 |         398 |       28 | -                   |
    |  40 |         431 |       76 | X                   |
    |  41 |         441 |       80 | X                   |
    |  42 |         452 |       72 | X                   |
    |  43 |         463 |       45 | -                   |
    |  44 |         474 |       33 | -                   |
    | ... |         ... |   ...    | ...                 |
    |  78 |         840 |       29 | -                   |
    |  79 |         851 |       38 | -                   |
    |  80 |         861 |       52 | X                   |
    |  81 |         872 |       72 | X                   |
    |  82 |         883 |       75 | X                   |
    |  83 |         894 |       65 | X                   |
    |  84 |         904 |       44 | X                   |
    |  85 |         915 |       33 | -                   |
    |  86 |         926 |       26 | -                   |
    | ... |         ... |   ...    | ...                 |
    | 118 |        1270 |       21 | -                   |
    | 119 |        1281 |       28 | -                   |
    | 120 |        1292 |       37 | X                   |
    | 121 |        1303 |       52 | X                   |
    | 122 |        1314 |       69 | X                   |
    | 123 |        1324 |       70 | X                   |
    | 124 |        1335 |       58 | X                   |
    | 125 |        1346 |       39 | X                   |
    | 126 |        1357 |       29 | X                   |
    | 127 |        1367 |       22 | -                   |
    | 128 |        1378 |       17 | -                   |
    """
    i = 0
    partial = {'n': 1, 'f': None}
    integral = 0
    while True:
        partial['f'] = partial['n'] * f0
        x_min, x_max = create_threshold(partial['f'], cents=cents)

        while (i < len(frequencies)) and (frequencies[i] < x_min):
            i += 1

        while (i < len(frequencies)) and (frequencies[i] <= x_max):
            integral += spectrum[i]
            i += 1

        if not (i < len(frequencies)):
            break

        partial['n'] += 1

    return integral


def old_stuff():
    """backup: old lingering stuff"""
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


def get_lingling_measures(file, top_db=TOP_DB):
    """Return the history of lingling measurements."""
    y, f0_series = get_f0_series(file)

    amplitude = np.abs(librosa.stft(y))
    spectrum = librosa.amplitude_to_db(amplitude, ref=np.max, top_db=top_db)
    # Shift from the interval -80..0 to the interval 0..80.
    spectrum += TOP_DB
    frequencies = librosa.fft_frequencies()

    # Avoid tails because of potential artifacts.
    lingling_measures = []
    for i in range(spectrum.shape[1]):
        if math.isnan(f0_series[i]): continue
        peaks_integral = \
            integrate_peaks(f0_series[i], frequencies, spectrum[:,i])
        total_integral = spectrum[:,i].sum()

        lingling_measures.append(peaks_integral / total_integral)

    return lingling_measures


def main():

    # Some questions for when I’m working with the f0 series:
    # Q: do I want/need to calculate this every time (note) (what about vibrato?)?
    # Q: should I build a database of f0’s and corresponding thresholds?
    # A: here I think definitely
    # Q: should I round the values to reduce the possible f0’s?
    # Q: in the resolution that I use here for frequencies, what’s the sensible rounding scheme (if any)?

    sounds = [
        '/home/rafa/dev/sound/440-10-partials/440-10-partials.wav',
        '/home/rafa/dev/sound/players/hh/hh.wav',
        '/home/rafa/dev/sound/players/me/me.wav']

    x = []
    for sound in sounds:
        x.append({'file': sound,
                  'l2m': get_lingling_measures(sound)})

    print(f'{x=}')


if __name__ == '__main__':
    main()
