#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tensorflow as tf
import os , sys
from sig_processing import read_file,remove_silence_file
import time
#!/usr/bin/env python
#-*- coding: utf-8 -*-
#list phonemes arabe
phonemes_list = ['أ','ب','ت','ث','ج','ح','خ','د','ذ','ر','ز','س','ش','ص','ض','ط','ع','غ'
               ,'ف','ق','ك','ل','م','ن','ه','و','ي']
#list words arabe
words_list = ['أكل','شرب','قام','لعب','نام','الشمس','القمر','أب','أم','قط','كلب','القلم','الكتاب','تونس','أبيض']
saver_phonemes = None   #phoenme'saver object
saver_words = None      #word'saver object
#hidden layers operations
def multilayer_perceptron(x, all_vars):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x, all_vars[0]), all_vars[5])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, all_vars[1]), all_vars[6])
    layer_2 = tf.nn.relu(layer_2)

    layer_3 = tf.add(tf.matmul(layer_2, all_vars[2]), all_vars[7])
    layer_3 = tf.nn.relu(layer_3)
    layer_4 = tf.add(tf.matmul(layer_3, all_vars[3]), all_vars[8])
    layer_4 = tf.nn.relu(layer_4)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_4, all_vars[4]) + all_vars[9]
    return out_layer

#this is the main function that we'll call it in the server to recognize the sample
def recognition(x,test,checkpoint_dir,new_saver):
    with tf.Session() as sess:
        new_saver.restore(sess, tf.train.latest_checkpoint(checkpoint_dir))
        all_vars = tf.get_collection('vars')
        pred = multilayer_perceptron(x, all_vars)
        predic = tf.argmax(pred, 1)
        ind = predic.eval(feed_dict={x: [test]})
    return ind[0]

#we'll call it in the server to recognize the phoneme sample
#will return the result (phoneme)
def phoneme_recognition(file,save_dir,val):
    global saver_phonemes
    # remove the silence at the beginning and at the end of the wave files
    remove_silence_file(file)
    test = read_file(file,val)  #read the file and extract the features using mfcc
    x = tf.placeholder("float", [None, val])
    ind = recognition(x,test,save_dir,saver_phonemes)
    os.remove(file)
    return phonemes_list[ind]

#we'll call it in the server to recognize the word sample
#will return the result (word)
def words_recognition(file,save_dir,input):
    global saver_words
    # remove the silence at the beginning and at the end of the wave files
    remove_silence_file(file)
    test = read_file(file,input)    #read the file and extract the features using mfcc
    x = tf.placeholder("float", [None, input])
    ind = recognition(x, test, save_dir, saver_words)
    os.remove(file)
    return words_list[ind]

#we'll call it in the server to load words' recogntion model
def recog_words(save_dir):
    global saver_words
    tf.reset_default_graph()
    saver_words = tf.train.import_meta_graph(save_dir+'model.meta')

#we'll call it in the server to load phonemes' recogntion model
def recog_phonemes(save_dir):
    global saver_phonemes
    tf.reset_default_graph()
    saver_phonemes = tf.train.import_meta_graph(save_dir+'model.meta')
