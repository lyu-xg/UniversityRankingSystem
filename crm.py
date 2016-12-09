# -*- coding: utf-8 -*
__author__ = 'wangdiyi'

import numpy as np
import random


RElATION_SIZE = 5
FEATURE_SIZE = 5
WEIGHT_SIZE = FEATURE_SIZE

LEARNING_RATE = 0.01
LAMBDA = 0.001
CONFS = {} # Dictionary for relative vectors, key is the name of conference
             # RElATION_SIZE size is 5 for each.
SCHOOLS = {} # Dictionary for relative vectors, key is the name of schools name.
             # RElATION_SIZE size is 5 for each.
TRAIN = []
VALID = []
TEST = []
WEIGHT_VECTOR = np.random.randn(WEIGHT_SIZE) * 0.5



def pre_data():


def train():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    #
    for data in TRAIN:
        real_hit = data[2]* 1.0
        school_vector = SCHOOLS[data[0][0]]
        conf_vector = CONFS[data[0][1]]
        f0 = np.dot (school_vector,conf_vector)
        feature_vector = np.zeros((1, FEATURE_SIZE))
        predict_hit = np.dot(feature_vector,WEIGHT_VECTOR)
        diff = real_hit - predict_hit


def test():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    total_diff = 0.0
    for data in TEST:

        real_hit = data[2] * 1.0
        school_vector = SCHOOLS[data[0][0]]
        conf_vector = CONFS[data[0][1]]
        f0 = np.dot(school_vector, conf_vector)
        feature_vector = np.zeros((1, FEATURE_SIZE))
        predict_hit = np.dot(feature_vector, WEIGHT_VECTOR)
        diff = real_hit - predict_hit
        total_diff += diff


def valid():


def learn():


def main():

    print "LEARNING_RATE = %f" % LEARNING_RATE
    print "LAMBDA = %f" % LAMBDA
	pre_data()
	learn()


if __name__ == '__main__':
    main()


