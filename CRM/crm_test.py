# -*- coding: utf-8 -*
# __author__ = 'wangdiyi'
import numpy as np
from math import *
from alldata import dataset
from affiliations import affiliationIDs
import time

LEARNING_RATE = 0.00001
LAMBDA = 0.01
TRAIN = []
TEST = []
# WEIGHT_VECTOR = np.random.randn(6)
WEIGHT_VECTORS = {}

TRUE_RANK_2014 = {}
TRUE_RANK_2015 = {}

IDCG_2014 = 0.0
IDCG_2015 = 0.0


def pre_data(conf):

    global LENGTH_TEST
    global LENGTH_TRAIN
    global TRUE_RANK_2014
    global TRUE_RANK_2015
    global IDCG_2014
    global IDCG_2015
    global WEIGHT_VECTORS

    whole_rank_2014 = {}
    whole_rank_2015 = {}

    for key in affiliationIDs:
        f_2011 = dataset[(key, conf, '2011')]
        f_2012 = dataset[(key, conf, '2012')]
        f_2013 = dataset[(key, conf, '2013')]
        f_2014 = dataset[(key, conf, '2014')]
        f_2015 = dataset[(key, conf, '2015')]
        WEIGHT_VECTORS[(key,conf)] = np.zeros(6)
        whole_rank_2014[key] = f_2014[5]
        whole_rank_2015[key] = f_2015[5]

        train_feature = list_add(f_2011,f_2012, f_2013)
        test_feature = list_add(f_2012, f_2013, f_2014)

        train_data = [key,train_feature,f_2014[5]]
        test_data = [key,test_feature,f_2015[5]]

        TRAIN.append(train_data)
        TEST.append(test_data)


    # the sorted list of key according to its value.
    # true top 20 school in 2014 and 2015
    rank_2014 = sorted(whole_rank_2014, key = whole_rank_2014.__getitem__)[::-1][:20]
    rank_2015 = sorted(whole_rank_2015, key = whole_rank_2015.__getitem__)[::-1][:20]

    # build up the dictionary for top 20 school
    # TRUE_RANK["CMU"] = (rank_value, rank_position)
    for i in range(len(rank_2014)):
        TRUE_RANK_2014[rank_2014[i]] = (whole_rank_2014[rank_2014[i]],i+1)

    for school in TRUE_RANK_2014:
        IDCG_2014 += TRUE_RANK_2014[school][0]/(log(TRUE_RANK_2014[school][1]+1)/log(2))

    for i in range(len(rank_2015)):
        TRUE_RANK_2015[rank_2015[i]] = (whole_rank_2015[rank_2015[i]],i+1)

    for school in TRUE_RANK_2015:
        IDCG_2015 += TRUE_RANK_2015[school][0]/(log(TRUE_RANK_2015[school][1]+1)/log(2))

    return

def list_add(l1,l2,l3):
    result = []
    for i in range(len(l1)):
        result.append(l1[i]+l2[i]+l3[i])
    return result


def train(conf):

    global WEIGHT_VECTORS

    whole_rank_2014 = {}
    total_diff = 0.0
    for data in TRAIN:
        weight = WEIGHT_VECTORS[(data[0],conf)]
        real_score = data[2] * 1.0
        feature_vector = np.array(data[1])
        predict_score = np.dot(feature_vector,weight)
        whole_rank_2014[data[0]] = predict_score
        diff = predict_score - real_score

        # calculate delta for w c_j s_i
        dw = diff * feature_vector
        total_diff += abs(diff)
        # update
        WEIGHT_VECTORS[(data[0], conf)] += -LEARNING_RATE*(dw + LAMBDA*weight)

    rank_result = sorted(whole_rank_2014, key=whole_rank_2014.__getitem__)[::-1]
    result = evalutate(rank_result, IDCG_2014,TRUE_RANK_2014)
    print "total error on train:%f" % total_diff
    print "NDCG@20 on train %f" %result
    return


def test(conf):

    global WEIGHT_VECTORS

    whole_rank_2015 = {}
    total_diff = 0.0
    for data in TEST:
        weight = WEIGHT_VECTORS[(data[0],conf)]
        real_score = data[2] * 1.0
        feature_vector = np.array(data[1])
        predict_score = np.dot(feature_vector, weight)
        whole_rank_2015[data[0]] = predict_score
        diff = predict_score - real_score
        total_diff += abs(diff)

    rank_result = sorted(whole_rank_2015,key=whole_rank_2015.__getitem__)[::-1]
    result = evalutate(rank_result,IDCG_2015,TRUE_RANK_2015)
    print "total error on test:%f" % total_diff
    print "NDCG@20 on test %f"%result
    return result


def evalutate(rank,i,dic):
    #
    #   rank is the predict rank
    #   Example: ['09E3EE34', '012E6F4E', '4CE6FC2D', '00FF56A8', '0489A984', '05E79D01', .....]
    #   i is the IDCG@20 value of 2014
    #   dic is true scores and it's true rank position.
    #       key : affiliationID, value:(score,rank)
    #   Example: {'0B845BA3': (7.249999999999999, 2), '00FF56A8': (5.633333333333334, 6),...}

    DCG = 0.0
    for school in dic:
        predict_rank = rank.index(school) + 1
        rel = dic[school][0]
        DCG += rel/(log(predict_rank+1)/log(2))

    NDCG = DCG/i

    return NDCG


def learn(conf):
    allresult = []
    for iteration in range(3):
        print "*****************************************************************"
        print "Iteration %d for %s" % (iteration+1,conf)
        print "Training..."
        train(conf)
        print "Testing"
        ndcg = test(conf)
        allresult.append(ndcg)
    OverallBest = max(allresult)

    # print rank_test[:100]
    # print rank_train[:100]

    return OverallBest


def basic_info():
    print "LEARNING_RATE = %f" % LEARNING_RATE
    print "LAMBDA = %f" % LAMBDA
    return


def main():
    start = time.clock()
    global TRAIN
    global TEST

    global IDCG_2014
    global IDCG_2015

    global TRUE_RANK_2014
    global TRUE_RANK_2015
    global WEIGHT_VECTORS

    conf_list = ['ICML','KDD','SIGIR','SIGMOD','SIGCOMM','FSE','MOBICOM','MM']
    finalresult = {}
    for conf in conf_list:
        pre_data(conf)
        finalresult[conf] = learn(conf)
        TRAIN = []
        TEST = []
        IDCG_2014 = 0.0
        IDCG_2015 = 0.0
        TRUE_RANK_2014 = {}
        TRUE_RANK_2015 = {}
        WEIGHT_VECTORS = {}
    print "****************************"
    basic_info()
    for conf in finalresult:
        print "NDCG@20 for %s is %f"%(conf,finalresult[conf])

    end = time.clock()
    print "Finish in %f s" %(end - start)

if __name__ == '__main__':
    main()


