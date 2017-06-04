import os
import scipy.io.wavfile as wavfile
from python_speech_features import mfcc
import numpy as np
import pickle as pk

#create label(one hot vector) by using the file names and the ooutput layer value
def create_label(files,dir,nb):
    # initialize label
    i = int(files[0].split('_', 1)[0]) - 1 #split the file name and take the first char
    y = np.insert(np.zeros(nb), i, 1)   # create one hot vector
    # creating label  as one-hot encodings
    for file in files[1:]:
        # create label
        i = int(file.split('_', 1)[0]) - 1  #split the file name and take the first char
        aux = np.insert(np.zeros(nb), i, 1) # create one hot vector
        y = np.vstack((y, aux)) #add the vecor to the label(vector of vectors)
    return y


# extracting  feature ( using mfcc)
#return features and the max length vector(the longest phonme/word)
def wav_to_mfcc(sig_rate):
    mfcc_list = []  #initialize the mfcc list
    max_mfcc_vector= 0  #initialize the max
    j = 0
    for i in sig_rate:
        #apply mfcc for each wave file and save it in the mfccc_list
        mfcc_list.append(mfcc(i[0], i[1],winlen=0.025,winstep=0.009,nfilt=20,numcep=13))
        #nfilt=20   0.730
        #ceplifter=0  0.78
        leng = len(mfcc_list[-1])
        #find the longest phoneme/word
        if(max_mfcc_vector<leng):
            k = j
            max_mfcc_vector  = leng
        j = j + 1
    return mfcc_list,max_mfcc_vector*len(mfcc_list[0][0]),k

#read wav failes and extract features from the signals
def read_files(files,dir):
    #read wav files
    signals_rates = []  #initialize the signals_rate list
    for file in files:
        rate, signal = wavfile.read(dir + "/" + file)   #read the file
        signals_rates.append([signal, rate])    #add the file to the list
    # extracting  feature(using mfcc) from wav files (sig_rate)
    # mfcc_list is a list of vector of size NUMFRAMES by numcep
    # max_mfcc_vector is the max of mfcc_list size of vectors
    mfcc_list, max_mfcc_vector,j = wav_to_mfcc(signals_rates)
    return mfcc_list,max_mfcc_vector

'''create feactures
make sure that input  the data have the same length
if a sample less than the max then we extend the vector by zeros'''

def create_feactures(mfcc_list,max):
    # initialize the feactures
    #mfcc is a vector of vector so we need to reshape it to a simple vector
    features = np.array(mfcc_list[0]).reshape(-1)
    m = len(features)
    while (m <= max):
        features = np.append(features, 0)
        m = m + 1
    if(m>max):
        features = features[0:max]
    for i in mfcc_list[1:]:
        aux = np.array(i).reshape(-1)
        m = len(aux)
        while (m <= max):
            aux = np.append(aux, 0)
            m = m + 1
        if (m > max):
            aux = aux[0:max]
        features = np.vstack((features, aux))
    print("create feac")
    return features

#create data (x+y)
def create_data(x,y):
    data=[]
    for i in range(len(y)):
        data.append([x[i],y[i]])
    return data











      ###44100  10000

