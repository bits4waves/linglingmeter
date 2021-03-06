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


def integrate_whole(f0, frequencies, spectrum, cents=THRESHOLD_CENTS):
    """Integrate the “whole”, the curve of interest.

    It may be the whole curve or just the partials."""
    x_min, _ = create_threshold(f0, cents=cents)

    i = 0
    while (i < len(frequencies)) and (frequencies[i] < x_min):
        i += 1

    return spectrum[i:].sum()


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
        total_integral = \
            integrate_whole(f0_series[i], frequencies, spectrum[:,i])
        lingling_measures.append(peaks_integral / total_integral)

    return lingling_measures


def get_l2ms(x):
    """Return the lingling measurements."""
    l2ms = []
    for d in x:
        l2ms.append(d['l2m'])

    return l2ms


def plot_x(x):

    import matplotlib
    import matplotlib.pyplot as plt
    import pandas as pd

    matplotlib.use('gtk3agg')

    fig, axs = plt.subplots(3, 1)

    i = 311
    for y in x:
        plt.subplot(i)
        plt.xlabel('Time')
        plt.ylabel('LingLing measure')
        plt.ylim(0, 0.85)
        plt.plot(y['l2m'], label=y['file'])
        # plot the moving window average
        pd.Series(y['l2m']).rolling(window=7).mean().plot(style='k')
        plt.legend()
        i += 1

    plt.show()


def main():

    # Some questions for when I’m working with the f0 series:
    # Q: do I want/need to calculate this every time (note) (what about vibrato?)?
    # Q: should I build a database of f0’s and corresponding thresholds?
    # A: here I think definitely
    # Q: should I round the values to reduce the possible f0’s?
    # Q: in the resolution that I use here for frequencies, what’s the sensible rounding scheme (if any)?
    # Q: should I arrange it so that the synthesized sound have the max score?

    debug = True

    if debug:
        suffix = '-debug'
    else:
        suffix = ''

    sounds = [
        '/home/rafa/dev/sound/players/hh/npr/01/01' + suffix + '.wav',
        '/home/rafa/dev/sound/players/hh/npr/02/02' + suffix + '.wav',
        '/home/rafa/dev/sound/players/hh/npr/05/05' + suffix + '.wav',
        ]

    x = []
    for sound in sounds:
        print(f'Processing {sound}')
        x.append({'file': sound,
                  'l2m': get_lingling_measures(sound)})

    plot_x(x)


if __name__ == '__main__':
    main()
