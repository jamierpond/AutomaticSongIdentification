import librosa
import numpy as np
from skimage.feature import peak_local_max
from inverted_list import *
from matplotlib import pyplot as plt


def get_constellation(input_audio, shouldPlot=False):
    spectrogram = np.abs(librosa.stft(input_audio, n_fft=2048,window='hann',win_length=2048,hop_length=256))
    constellation = peak_local_max(np.log(spectrogram), min_distance=10, threshold_rel=0.05, indices=False)
    if shouldPlot:
        plt.figure(figsize=(10, 5))
        plt.imshow(constellation, cmap=plt.cm.gray_r, origin='lower')
        plt.show()
    return constellation



# Testing.
# y, sr = librosa.load(os.path.join('database_recordings/classical.00004.wav'))
# get_constellation(y, False)
