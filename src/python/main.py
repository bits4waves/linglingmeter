import librosa

VIOLIN_MIN_F=librosa.note_to_hz('G3')
VIOLIN_MAX_F=librosa.note_to_hz('E7')

def get_pitch(snd_filename, fmin=VIOLIN_MIN_F, fmax=VIOLIN_MAX_F):
    """Extract f0 from sound file."""
    y, sr = librosa.load(snd_filename)
    f0, voiced_flag, voiced_probs = \
        librosa.pyin(y, fmin=VIOLIN_MIN_F, fmax=VIOLIN_MAX_F)

    return f0

pitch = get_pitch('/home/rafa/sci/sound/440/440.wav')
pass
