import librosa

VIOLIN_MIN_F=librosa.note_to_hz('G3')
VIOLIN_MAX_F=librosa.note_to_hz('E7')
FIFTY_CENTS_BWD = pow(2, -50/1200)
FIFTY_CENTS_FWD = pow(2, 50/1200)


def get_pitch_series(snd_filename, fmin=VIOLIN_MIN_F,
                     fmax=VIOLIN_MAX_F):
    """Extract f0 history from sound file."""
    y, sr = librosa.load(snd_filename)
    f0, voiced_flag, voiced_probs = \
        librosa.pyin(y, fmin=VIOLIN_MIN_F, fmax=VIOLIN_MAX_F)

    return y, f0


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
