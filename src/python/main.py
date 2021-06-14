import librosa

VIOLIN_MIN_F=librosa.note_to_hz('G3')
VIOLIN_MAX_F=librosa.note_to_hz('E7')

y, sr = librosa.load('/home/rafa/sci/sound/0/0.wav')
f0, voiced_flag, voiced_probs = \
    librosa.pyin(y, fmin=VIOLIN_MIN_F, fmin=VIOLIN_MAX_F)
