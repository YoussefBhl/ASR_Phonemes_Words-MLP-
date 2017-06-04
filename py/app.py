#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import time
from shutil import rmtree
from recognition import phoneme_recognition,words_recognition,recog_phonemes,recog_words
from flask import Flask, render_template, request,redirect
from mlp import train_model
import pickle


#list of phonemes'file
list_phonemes= ['1_A','2_B','3_T','4_TH','5_J','6_7','7_KH','8_D','9_TH','10_R','11_Z','12_S',
                '13_CH','14_SS','15_DH','16_T','17_3','18_GH','19_F','20_9','21_K','22_L',
                '23_M','24_N','25_H','26_W','27_Y']


#list of words'file
list_mots = ['1_AKALA','2_CHARIBA','3_9ama','4_la3iba','5_NEMA','6_ELCHAMES','7_EL9AMER','8_ABON',
             '9_OMON','10_9ITON','11_kelbon','12_EL9aLEM','13_ELKITEB','14_TUNIS','15_ABYEDH']



repeat = 1  #the values of phoeme or word repetition number
indice = 0  #the index of phoeme or word in the list
corpus_name = ""    #the corpus name set it by the user
phonemes_dir = ""   #phonemes'directory where the phonemes ( wav files)  will be saved to create corpus
words_dir = ""      #words'directory where the phonemes ( wav files)  will be saved to create corpus
phonemes_selected = False   #takes true if phonemes option selected else it takes true
words_selected = False      #takes true if words option selected else it takes true

'''return true if corpus name already exists ekse it return false '''
def coprus_name_exist(name):
    file = open("txt/corpus_names.txt", 'r')
    for i in file.readlines():
        if(i.strip() == name):
            file.close()
            return True
    file.close()
    return False

#initialize flask
app = Flask(__name__, template_folder='../html-templates', static_folder='../assets')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('accueil.html')

@app.route('/recognition')
def recognition():
    return render_template('recognition.html')
@app.route('/corpus')
def corpus():
    return render_template('corpus.html')

@app.route('/propos')
def propos():
    return render_template('propos.html')
@app.route('/contact-us')
def contact():
    return render_template('contact-us.html')
@app.route('/quitter')
def quitter():
    return render_template('quitter.html')
@app.route('/choix-utilisateur')
def choose():
    return render_template('chooseUser.html')


@app.route('/analyze_phoneme', methods=['POST'])
def analyze():
    global phonemes_selected,words_selected

    if(phonemes_selected == False):
        recog_phonemes("saves/" + corpus_name + '/phonemes/') #load phonemes moadel
        phonemes_selected = True
        words_selected = False

    file =  request.files['data']
    filename = str(int(time.time())) +".wav"    #takes the time value
    #os.mknod(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  #save the temporary file

    '''input is for neural net input layer
    each user have a input file (pickle file) for phoneme model'''
    input = pickle.load(open("saves/" + corpus_name + '/phonemes/input.p', "rb"))
    return phoneme_recognition("uploads" + "/" + filename,"saves/" + corpus_name + '/phonemes/',input)


@app.route('/analyze_mot', methods=['POST'])
def analyze1():
    global phonemes_selected, words_selected

    if (words_selected == False):
        recog_words("saves/" + corpus_name + '/words/')  # load words moadel
        words_selected = True
        phonemes_selected = False

    file =  request.files['data']
    filename = str(int(time.time())) +".wav"     #takes the time value

   # os.mknod(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename )) #save the temporary file

    '''input is for neural net input layer
        each user have a input file pickle file) for words model '''
    input = pickle.load(open("saves/" + corpus_name + '/words/input.p', "rb"))
    return words_recognition("uploads" + "/" + filename,"saves/" + corpus_name + '/words/',input)

@app.route('/analyze_paragraphe', methods=['POST'])
def analyze2():
    return "Commig soon"

@app.route('/contact', methods=['POST'])
def handel():
    val = request.form['validation']
    if(val == 'true'):
        #save forms to file in the server
        filename = "txt/messages.txt"
        if  os.path.isfile(filename):
            file = open(filename, "a")
        else:
            file = open(filename, "w")
        name = request.form['name']
        email = request.form['email']
        tel = request.form['tel']
        message = request.form['message']
        file.write("name & lastname : " + name + " \n")
        file.write("email : " + email +"\n")
        file.write("tel : " + tel +"\n")
        file.write("message : " + message +"\n")
        file.write('-' * 30)
        file.close()
    return "ok"

@app.route('/oldUser', methods=['POST'])
def oldUser():
    global corpus_name
    #check if the corpus's name exist or not
    if (not coprus_name_exist(request.form['name'])):
        return "utilisateur introuvable"
    else:
        corpus_name = request.form['name']
        return "ok"

@app.route('/newUser', methods=['POST'])
def newUser():
    global corpus_name,words_dir,phonemes_dir
    # check if the corpus's name exist or not
    if (coprus_name_exist(request.form['name'])):
        return "utilisateur deja existe"
    else:
        #if the corpus's name doesn't exist then
        # add it to the list and
        file = open("txt/corpus_names.txt", 'a')
        corpus_name = request.form['name']
        file.write("\n"+corpus_name)
        file.close()
        #create the directories for this new corpus
        if not os.path.exists(app.config['UPLOAD_FOLDER']+'/'+corpus_name):
            os.makedirs(app.config['UPLOAD_FOLDER'] + '/' + corpus_name)
            os.makedirs('saves/' + corpus_name)
            words_dir = app.config['UPLOAD_FOLDER'] + '/' + corpus_name + '/words'
            os.makedirs(words_dir)
            phonemes_dir = app.config['UPLOAD_FOLDER'] + '/' + corpus_name + '/phonemes'
            os.makedirs(phonemes_dir)
        return "ok"

@app.route('/savecorpus', methods=['POST'])
def corp():
    global indice,repeat,phonemes_dir,words_dir
    file =  request.files['data']
    '''this code makes the synchronization between the voice saved by the user
    then send it via javascript (ajax) and the server to make sure that the files'name are correct
    (exemple 1_A1 1_A2 represent the first phoneme 'A') and ready to be used in the neural net'''

    if(indice<27):  #the file is a phoneme then save the wav file with name that represent the phoneme
        filename = str(list_phonemes[indice])+ str(repeat) +".wav"
        filename = str(list_phonemes[indice])+ str(repeat) +".wav"
        file.save(os.path.join(phonemes_dir, filename))

    elif(indice<42):    #the file is a word then save the wav file with name that represent the word
        filename = str(list_mots[indice-27]) + str(repeat) + ".wav"
        file.save(os.path.join(words_dir, filename))

    if(repeat == 5):    #if the repeatation ends then move on to the next word/phoneme
        indice += 1
        repeat = 0
    if (indice == 42):  #the recording is done and the corpus(phonemes & words) are ready. so we train our models
        #first train phonemes's model
        train_model(phonemes_dir, "saves/" + corpus_name + '/phonemes', 26)
        # And second train words's model
        train_model(words_dir, "saves/" + corpus_name + '/words', 14)
        #after the models are trained than we delete the corpus
        rmtree(app.config['UPLOAD_FOLDER'] + '/' + corpus_name)
        return "done"

    repeat += 1
    #os.mknod(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "ok"

app.run('0.0.0.0', 5000)