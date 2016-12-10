# -*- coding: utf-8 -*
__author__ = 'wangdiyi'

import numpy as np
import random
import sys

RElATION_SIZE = 5
FEATURE_SIZE = 5
WEIGHT_SIZE = FEATURE_SIZE

LEARNING_RATE = 0.001
LAMBDA = 0.001
CONFS = {} # Dictionary for relative vectors, key is the name of conference
             # RElATION_SIZE size is 5 for each.
SCHOOLS = {} # Dictionary for relative vectors, key is the name of schools name.
             # RElATION_SIZE size is 5 for each.
TRAIN = []
# VALID = []
TEST = []
WEIGHT_VECTORS = {}



def pre_data():
    # randomly init CONFS and SCHOOLS
    school_list = ["CMU","NEU", "NYU","UCB","UCI","BUPT"]
    conf_list = ["KDD","ICDM","CVPR","AAAI","ICDL","ICML"]
    # [[school_name, conference_name], [f1, f2, f3, f4], X]

    for i in range(1000):
        school = school_list[random.randint(0, len(school_list)-1)]
        conf = conf_list[random.randint(0, len(conf_list)-1)]
        features = np.random.rand(4)
        X = np.random.random_integers(20)
        data = [[school,conf],features,X]
        if i <= 800:
            TRAIN.append(data)
        else:
            TEST.append(data)
    for school in school_list:
        s = np.random.randn(RElATION_SIZE) * 0.5
        SCHOOLS[school] = s
    for conf in conf_list:
        c = np.random.randn(RElATION_SIZE) * 0.5
        CONFS[conf] = c
    for school in school_list:
        for conf in conf_list:
            WEIGHT_VECTORS[(school,conf)] = np.random.randn(WEIGHT_SIZE) * 0.5
    return

def train():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    global WEIGHT_VECTORS
    global CONFS
    global SCHOOLS

    total_diff = 0.0
    for data in TRAIN:
        real_hit = data[2]* 1.0
        school_vector = SCHOOLS[data[0][0]]
        conf_vector = CONFS[data[0][1]]
        weight = WEIGHT_VECTORS[tuple(data[0])]
        f0 = np.dot (school_vector,conf_vector)
        feature_vector = np.array([f0])
        feature_vector = np.concatenate((feature_vector,data[1]),axis = 0)
        predict_hit = np.dot(feature_vector,weight)
        diff = real_hit - predict_hit
        total_diff += diff

        #calculate delta for w c_j s_i
        ds = 2 * diff * weight[0] * conf_vector
        dc = 2 * diff * weight[0] * school_vector
        dw = 2 * diff * feature_vector

        #update
        SCHOOLS[data[0][0]] += LEARNING_RATE*(ds + LAMBDA*school_vector)
        CONFS[data[0][1]] += LEARNING_RATE*(dc + LAMBDA*conf_vector)
        WEIGHT_VECTORS[tuple(data[0])] += LEARNING_RATE*(dw + LAMBDA*weight)

    return total_diff


def test():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]

    global WEIGHT_VECTORS
    global CONFS
    global SCHOOLS

    total_diff = 0.0
    for data in TEST:

        real_hit = data[2] * 1.0
        school_vector = SCHOOLS[data[0][0]]
        conf_vector = CONFS[data[0][1]]
        weight = WEIGHT_VECTORS[tuple(data[0])]
        f0 = np.dot(school_vector, conf_vector)
        feature_vector = np.array([f0])
        feature_vector = np.concatenate((feature_vector, data[1]), axis=0)
        predict_hit = np.dot(feature_vector, weight)
        diff = real_hit - predict_hit
        total_diff += diff
    print "total error on test:%f" % total_diff


# def valid():
#
#     global WEIGHT_VECTOR
#
#     total_diff = 0.0
#     for data in VALID:
#         real_hit = data[2] * 1.0
#         school_vector = SCHOOLS[data[0][0]]
#         conf_vector = CONFS[data[0][1]]
#         f0 = np.dot(school_vector, conf_vector)
#         feature_vector = np.zeros((1, FEATURE_SIZE))
#         predict_hit = np.dot(feature_vector, WEIGHT_VECTOR)
#         diff = real_hit - predict_hit
#         total_diff += diff
#     print "Current Error in sum:"
#     print total_diff


# def evaluate():
# to evaluate the rank accuracy of model.


def learn():

    # f_handler = open('h40.txt', 'a')
    # sys.stdout = f_handler

    for iter in range(300):
        print "Iter %d" % iter
        print "Training..."
        loss = train()
        print "total error on train:%f"%loss

        print "Testing"
        test()
        #f_handler.close()


def main():

    print "LEARNING_RATE = %f" % LEARNING_RATE
    print "LAMBDA = %f" % LAMBDA
    pre_data()
    learn()

if __name__ == '__main__':
    main()


