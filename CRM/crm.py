# -*- coding: utf-8 -*
__author__ = 'wangdiyi'

import numpy as np
import random


RElATION_SIZE = 5
FEATURE_SIZE = 5
WEIGHT_SIZE = FEATURE_SIZE

LEARNING_RATE = 0.01
LAMBDA = 0.01
TRAIN = []
TEST = []
VALID = []
WEIGHT_VECTORS = {}



def pre_data():
    # randomly init CONFS and SCHOOLS
    school_list = range(100)
    conf_list = ["KDD","ICDM","CVPR","AAAI","ICDL","ICML"]
    # [[school_name, conference_name], [f1, f2, f3, f4], X]

    for i in range(1000):
        school = school_list[random.randint(0, len(school_list)-1)]
        conf = conf_list[random.randint(0, len(conf_list)-1)]
        features = np.random.randn(4)
        X = np.random.random_integers(10)
        data = [[school,conf],features,X]
        TRAIN.append(data)

    for school in school_list:
        for conf in conf_list:
            WEIGHT_VECTORS[(school,conf)] = np.random.randn(WEIGHT_SIZE) * 0.5
    return

def train():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    global WEIGHT_VECTORS


    total_diff = 0.0
    for data in TRAIN:
        real_hit = data[2]* 1.0
        weight = WEIGHT_VECTORS[tuple(data[0])]
        f0 = 1
        feature_vector = np.array([f0])
        feature_vector = np.concatenate((feature_vector,data[1]),axis = 0)
        predict_hit = np.dot(feature_vector,weight)
        diff = predict_hit - real_hit
        total_diff += abs(diff)

        # calculate delta for w c_j s_i
        dw = 2 * diff * feature_vector

        # update
        WEIGHT_VECTORS[tuple(data[0])] -= LEARNING_RATE*(dw + LAMBDA*weight)
        # print WEIGHT_VECTORS
    return total_diff/800


def test():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]

    total_diff = 0.0
    for data in TEST:
        real_hit = data[2] * 1.0
        weight = WEIGHT_VECTORS[tuple(data[0])]
        f0 = 1
        feature_vector = np.array([f0])
        feature_vector = np.concatenate((feature_vector, data[1]), axis=0)
        predict_hit = np.dot(feature_vector, weight)
        diff = real_hit - predict_hit
        total_diff += abs(diff)
    print "total error on test:%f" % (total_diff/200)


def valid(error):

    global WEIGHT_VECTORS
    global LEARNING_RATE

    total_diff = 0.0
    for data in VALID:
        real_hit = data[2] * 1.0
        weight = WEIGHT_VECTORS[tuple(data[0])]
        f0 = 1
        feature_vector = np.array([f0])
        feature_vector = np.concatenate((feature_vector, data[1]), axis=0)
        predict_hit = np.dot(feature_vector, weight)
        diff = real_hit - predict_hit
        total_diff += abs(diff)
    avg_error = (total_diff / 100)
    print "total error on valid:%f" % avg_error
    if avg_error>error:
        LEARNING_RATE *= 1.5
    else:
        LEARNING_RATE *= 0.5
    return error



# def evaluate():
# to evaluate the rank accuracy of model.


def learn():


    for iter in range(100):
        print "Iter %d" % iter
        print "Training..."
        loss = train()
        print "total error on train:%f" % loss
        # error = valid(pasterror)
        # pasterror = error
        #print "Testing"
        #test()

    return

def basic_info():
    print "LEARNING_RATE = %f" % LEARNING_RATE
    print "LAMBDA = %f" % LAMBDA
    return

def main():
    pre_data()
    basic_info()
    learn()

if __name__ == '__main__':
    main()


