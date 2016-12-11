# -*- coding: utf-8 -*
# __author__ = 'wangdiyi'
import numpy as np
from math import *

LENGTH_TRAIN = 0
LENGTH_TEST = 0

LEARNING_RATE = 0.001
LAMBDA = 0.1
TRAIN = []
TEST = []
WEIGHT_VECTOR = np.random.randn(5)

def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))

def pre_data():
    # randomly init CONFS and SCHOOLS
    # school_list = range(100)
    # conf_list = ["KDD","ICDM","CVPR","AAAI","ICDL","ICML"]
    # [[school_name, conference_name], [f1, f2, f3, f4], X]
   
    global LENGTH_TEST
    global LENGTH_TRAIN
    para = np.array([1,2,3,4,5])
    
    for i in range(1000):
        data = np.random.randint(10, size=5)
        label =  np.dot(para,data)
        label = sigmoid(label)
        data = [data,label]
        if i >=800:
            TEST.append(data)
        else: 
            TRAIN.append(data)

        

    LENGTH_TEST = len(TEST)
    LENGTH_TRAIN = len(TRAIN)

    return


def train():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    global WEIGHT_VECTOR

    
    total_diff = 0.0
    for data in TRAIN:
        real_score = data[1]
        feature_vector = data[0]
        predict_score = np.dot(feature_vector,WEIGHT_VECTOR)
        diff = predict_score - real_score
        
        # calculate delta for w c_j s_i
        dw = diff * feature_vector
        total_diff += abs (diff)

        # update
        WEIGHT_VECTOR += -LEARNING_RATE*(dw + LAMBDA*WEIGHT_VECTOR)
    print WEIGHT_VECTOR
    return total_diff/LENGTH_TRAIN


def test():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    whole_rank_2015 = {}
    total_diff = 0.0
    for data in TEST:
        real_score = data[1]
        feature_vector = data[0]
        predict_score = np.dot(feature_vector,WEIGHT_VECTOR)
        diff = predict_score - real_score
        total_diff += abs(diff)
    print "total error on test:%f" % (total_diff/LENGTH_TEST)

    # rank_result = sorted(whole_rank_2015,key=whole_rank_2015.__getitem__)
    # evalutate(rank_result,IDCG_2015,TRUE_RANK_2015)


def evalutate(rank,i,dic):
    DCG = 0.0
    for school in dic:
        predict_rank = rank.index(school) + 1
        rel = dic[school][0]
        DCG += rel/(log(predict_rank+1)/log(2))
    NDCG = DCG/i
    print NDCG
    return



def learn():

    for iteration in range(100):
        print "*****************************************************************"
        print "Iter %d" % iteration
        print "Training..."
        loss = train()
        print "total error on train:%f" % loss

        print "Testing"
        test()

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


