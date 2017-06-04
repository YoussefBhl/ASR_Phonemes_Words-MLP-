
import os
import numpy as np
import random
import load_data
from remove_silence import remove_silence
import tensorflow as tf
import pickle
def normilaze_data(x):
    return np.where(x<0, -x/ x.min(), x/ x.max())

#hidden layers operations
def multilayer_perceptron(x, weights, biases,_droupout):
    #1 Hidden layer with RELU activation & droupout
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    layer_1 = tf.nn.dropout(layer_1,keep_prob=_droupout)
    #2 Hidden layer with RELU activation & droupout
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    layer_2 = tf.nn.dropout(layer_2,keep_prob=_droupout)
    #3 Hidden layer with RELU activation & droupout
    layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'])
    layer_3 = tf.nn.relu(layer_3)
    layer_3 = tf.nn.dropout(layer_3, keep_prob=_droupout)
    #4 Hidden layer with RELU activation & droupout
    layer_4 = tf.add(tf.matmul(layer_3, weights['h4']), biases['b4'])
    layer_4 = tf.nn.relu(layer_4)
    layer_4 = tf.nn.dropout(layer_4, keep_prob=_droupout)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_4, weights['out']) + biases['out']
    return out_layer
'''this function sparate the data to feactures and labels'''
def separate_data(data):
    fea = np.array(data[0][0])
    label = np.array(data[0][1])
    for i in range(1,len(data)):
        fea = np.vstack((fea,data[i][0]))
        label = np.vstack((label, data[i][1]))
    return   fea,label

#randomy shaffle the data
#we need for each iteration to shuffle the data
def shuffle_data(data):
    random.shuffle(data)
    fea = np.array(data[0][0])
    label = np.array(data[0][1])
    for i in range(1, len(data)):
        fea = np.vstack((fea, data[i][0]))
        label = np.vstack((label, data[i][1]))
    return fea, label

#return the next batch that the neural nets will use it
def train_next_batch(trainX,trainY,batch_size,next,len):
    if (next/batch_size == len/batch_size-1):
        return trainX[next:len], trainY[next:len]
    #case of the length of data not divide by batch
    return trainX[next:batch_size+next],trainY[next:batch_size+next]

#this is the main function that we'll call it in the server to train our model
#nb_rslt is used to create the labels(one hot vector) and the output class
# cuz the phonemes & words do't have the same output classification
def train_model(dir,save_dir,nb_rslt):
    #create dir to save on it the model (wights and the biases)
    # to be used next in the recognition
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        #os.makedirs(dir+"/new")
    #remove the silence at the beginning and at the end of the wave files
    remove_silence(dir, dir)
    files = os.listdir(dir)
    #create the labes named  trainY
    trainY = load_data.create_label(files, dir,nb_rslt)

    '''read the wave files and apply mfcc for each file the return the list of mfcc
    and the max_vector (the longest phoneme/word size which we 'll need it to make sure that
    all the vectors (input) has the same length'''
    mfcc_list, max_mfcc_vector = load_data.read_files(files, dir)
    # create the feactures named  trainX
    trainX = load_data.create_feactures(mfcc_list, max_mfcc_vector)
    # create dataset (trainX + trainY) which we'll use it to shuffle the date
    train_data = load_data.create_data(trainX, trainY)
    # Parameters
    learning_rate = 0.01
    training_epochs = 500
    batch_size = 30
    beta = 0.1
    display_step = 1
    dropout = .75
    # Network Parameters
    n_hidden_1 = 1000# 1st layer number of features
    n_hidden_2 = 900# 2nd layer number of features
    n_hidden_3 = 800# 3d layer number of features
    n_hidden_4 = 700# 4d layer number of features
    n_input = len(train_data[0][0]) #the length of the trainX'element
    n_classes =  nb_rslt+1 # total classes (27 phonemes) (15 words)

    # tf Graph input
    x = tf.placeholder("float", [None, n_input])
    y = tf.placeholder("float", [None, n_classes])
    keep_prob = tf.placeholder(tf.float32) #dropout (keep probability)

    # Store layers weight & bias
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1]),name="h1"),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2]),name="h2"),
        'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3]),name="h3"),
        'h4': tf.Variable(tf.random_normal([n_hidden_3, n_hidden_4]),name="h4"),
        'out': tf.Variable(tf.random_normal([n_hidden_4, n_classes]),name="hout")
    }
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1]),name="b1"),
        'b2': tf.Variable(tf.random_normal([n_hidden_2]),name="b2"),
        'b3': tf.Variable(tf.random_normal([n_hidden_3]),name="b3"),
        'b4': tf.Variable(tf.random_normal([n_hidden_4]),name="b4"),
        'out': tf.Variable(tf.random_normal([n_classes]),name="bout")
    }

    # Construct model
    pred = multilayer_perceptron(x, weights, biases,dropout)

    # Define loss and optimizer
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

    # Initializing the variables
    init = tf.global_variables_initializer()
    trainX,trainY = separate_data(train_data)
    train_len=len(trainX)

    # Add ops to save and restore all the variables.
    tf.add_to_collection('vars', weights['h1'])
    tf.add_to_collection('vars', weights['h2'])
    tf.add_to_collection('vars', weights['h3'])
    tf.add_to_collection('vars', weights['h4'])
    tf.add_to_collection('vars', weights['out'])

    tf.add_to_collection('vars', biases['b1'])
    tf.add_to_collection('vars', biases['b2'])
    tf.add_to_collection('vars', biases['b3'])
    tf.add_to_collection('vars', biases['b4'])
    tf.add_to_collection('vars', biases['out'])

    saver = tf.train.Saver()

    print ("TF RSLT")
    # Launch the graph
    acc_rslt = np.array(0)
    epoch_rslt = np.array(0)
    # save input layer value in file
    pickle.dump(n_input, open(save_dir+"/input.p", "wb"))
    with tf.Session() as sess:
        sess.run(init)
    # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(train_len/batch_size)
            #shuffle data
            trainX,trainY=shuffle_data(train_data)
            # Loop over all batches
            next=0
            for i in range(total_batch):
               # return the next batch
                batch_x, batch_y = train_next_batch(trainX,trainY,batch_size,next,train_len)
                # Run optimization op (backprop) and cost op (to get loss value)
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                              y: batch_y, keep_prob : dropout})
                # Compute average loss
                avg_cost += c / total_batch
                next += batch_size
            # Display logs per epoch step
            if epoch % display_step == 0:
                print ("Epoch:", '%04d' % (epoch+1), "cost=", \
                    "{:.9f}".format(avg_cost))

        #save the model
        save_path = saver.save(sess, save_dir+'/model')
        print ("Optimization Finished!")
    #reset the tensor graph which will be used next
    tf.reset_default_graph()
    print("Model saved in file: %s" % save_path)