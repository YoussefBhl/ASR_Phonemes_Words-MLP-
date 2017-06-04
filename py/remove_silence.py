import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
from pydub import AudioSegment
import os
import numpy as np
import scipy as sp
from scipy import signal

def detect_leading_silence(sound, silence_threshold=-28.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms
    leng = len(sound)
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms <=leng:
        trim_ms += chunk_size
    return trim_ms

def remove_silence(dir,new_dir):
    for file in os.listdir(dir):
        sound = AudioSegment.from_file(dir + "/" + file, format="wav")
        start_trim = detect_leading_silence(sound)
        end_trim = detect_leading_silence(sound.reverse())
        duration = len(sound)
        trimmed_sound = sound[start_trim:duration - end_trim]
        trimmed_sound.export(new_dir + "/" + file,format="wav")

