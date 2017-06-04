import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from pydub import AudioSegment
import os
import numpy as np
import scipy as sp
from scipy import signal
from python_speech_features import mfcc
#-45.0 windows
def detect_leading_silence(sound, silence_threshold=-28.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold:
        trim_ms += chunk_size


    return trim_ms

#remove the silence at the beginning and at the end of the wave files
def remove_silence_file(file):
    sound = AudioSegment.from_file(file, format="wav")
    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())
    duration = len(sound)
    trimmed_sound = sound[start_trim:duration - end_trim]
    #os.remove(file)
    trimmed_sound.export(file , format="wav")
   # os.remove(file)

'''read just a file which record it by the user
to make the recogniton ( this function will be used in recognition page)
if the sample less than the max then we extend the vector by zeros'''
def read_file(file,max):
    rate, signal = wavfile.read(file)
    signal = mfcc(signal,rate)
    signal = np.array(signal).reshape(-1)
    m = len(signal)
    while (m < max):
        signal = np.append(signal, 0)
        m = m + 1
    signal= signal[0:max]
    return signal