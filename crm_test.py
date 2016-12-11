# -*- coding: utf-8 -*
# __author__ = 'wangdiyi'
import numpy as np
from math import *

LENGTH_TRAIN = 0
LENGTH_TEST = 0

LEARNING_RATE = 0.01
LAMBDA = 0.1
TRAIN = []
TEST = []
WEIGHT_VECTOR = np.random.rand(5)

data_set = {("CMU","KDD"): [[1,1,1,1,1,1], [1,1,1,1,1,2], [1,1,1,1,1,3],[1,1,1,1,1,4], [1,1,1,1,1,5]]}
data_set[("NEU","KDD")] = [[1,1,1,1,1,-1], [1,1,1,1,1,-2], [1,1,1,1,1,3],[1,1,1,1,1,-4], [1,1,1,1,1,6]]
data_set[("NEU1","KDD")] = [[1,4,2,1,1,-1], [1,1,1,8,1,-2], [1,7,1,7,1,3],[1,1,6,1,1,1], [1,1,1,1,1,7]]
data_set[("NEU2","KDD")] = [[1,6,3,1,1,-1], [1,7,3,1,1,-2], [1,1,1,1,8,3],[1,1,1,18,1,2], [1,1,1,1,1,8]]
data_set[("NEU3","KDD")] = [[1,7,1,1,1,-1], [1,1,4,1,1,-2], [1,1,1,1,1,3],[1,1,1,1,1,3], [1,1,1,1,1,9]]

TRUE_RANK_2014 = {}
TRUE_RANK_2015 = {}
IDCG_2014 = 0.0
IDCG_2015 = 0.0

def pre_data():
    # randomly init CONFS and SCHOOLS
    # school_list = range(100)
    # conf_list = ["KDD","ICDM","CVPR","AAAI","ICDL","ICML"]
    # [[school_name, conference_name], [f1, f2, f3, f4], X]
    global data_set
    global LENGTH_TEST
    global LENGTH_TRAIN
    global TRUE_RANK_2014
    global TRUE_RANK_2015
    global IDCG_2014
    global IDCG_2015


    whole_rank_2014 = {}
    whole_rank_2015 = {}
    # data = {("CMU","KDD"):[[2011],[2012],[2013],[2014],[2015]]}
    # 2011 : [f1 f2 f3 f4 f5 ranking score]
    for key in data_set:
        conf = key[1]
        school = key[0]
        feature = data_set[key]
        if conf == "KDD":
            whole_rank_2014[school] = feature[3][5]
            whole_rank_2015[school] = feature[4][5]

            train_feature = list_add(feature[0],feature[1], feature[2])
            test_feature = list_add(feature[1], feature[2], feature[3])

            train_data = [key,train_feature[:5],feature[3][5]]
            test_data = [key, test_feature[:5], feature[4][5]]

            TRAIN.append(train_data)
            TEST.append(test_data)
        else:
            continue

    # the sorted list of key according to its value.
    # true top 20 school in 2014 and 2015
    rank_2014 = sorted(whole_rank_2014, key=whole_rank_2014.__getitem__)[::-1][:20]
    rank_2015 = sorted(whole_rank_2015, key=whole_rank_2015.__getitem__)[::-1][:20]

    # build up the dictionary for top 20 school
    # TRUE_RANK["CMU"] = (rank_value, rank_position)
    for key in range(len(rank_2014)):
        TRUE_RANK_2014[rank_2014[key]] = (whole_rank_2014[rank_2014[key]],key+1)

    for school in TRUE_RANK_2014:
        IDCG_2014 += TRUE_RANK_2014[school][0]/(log(TRUE_RANK_2014[school][1]+1)/log(2))

    for key in range(len(rank_2015)):
        TRUE_RANK_2015[rank_2015[key]] = (whole_rank_2015[rank_2015[key]],key+1)

    for school in TRUE_RANK_2015:
        IDCG_2015 += TRUE_RANK_2015[school][0]/(log(TRUE_RANK_2015[school][1]+1)/log(2))

    LENGTH_TEST = len(TEST)
    LENGTH_TRAIN = len(TRAIN)

    return


def list_add(l1,l2,l3):
    result = []
    for i in range(len(l1)):
        result.append(l1[i]+l2[i]+l3[i])
    return result


def train():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    global WEIGHT_VECTOR

    whole_rank_2014 = {}
    total_diff = 0.0
    for data in TRAIN:
        real_score = data[2] * 1.0
        feature_vector = np.array(data[1])
        predict_score = np.dot(feature_vector,WEIGHT_VECTOR)
        whole_rank_2014[data[0][0]] = predict_score
        diff = predict_score - real_score
        total_diff += diff*diff

        # calculate delta for w c_j s_i
        dw = diff * feature_vector

        # update
        WEIGHT_VECTOR += -LEARNING_RATE*(dw + LAMBDA*WEIGHT_VECTOR)
    rank_result = sorted(whole_rank_2014, key=whole_rank_2014.__getitem__)
    evalutate(rank_result, IDCG_2014,TRUE_RANK_2014)
    return total_diff/LENGTH_TRAIN


def test():
    # [[school_name,conference_name],[f1,f2,f3,f4],X]
    whole_rank_2015 = {}
    total_diff = 0.0
    for data in TEST:
        real_score = data[2] * 1.0
        feature_vector = np.array(data[1])
        predict_score = np.dot(feature_vector, WEIGHT_VECTOR)
        whole_rank_2015[data[0][0]] = predict_score
        diff = predict_score - real_score
        total_diff += abs(diff)
    print "total error on test:%f" % (total_diff/LENGTH_TEST)

    rank_result = sorted(whole_rank_2015,key=whole_rank_2015.__getitem__)
    evalutate(rank_result,IDCG_2015,TRUE_RANK_2015)


def evalutate(rank,i,dic):
    DCG = 0.0
    for school in dic:
        predict_rank = rank.index(school) + 1
        rel = dic[school][0]
        DCG += rel/(log(predict_rank+1)/log(2))
    NDCG = DCG/i
    print NDCG
    return

    return


def learn():

    for iteration in range(100):
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
    print TRUE_RANK_2014
    print TRUE_RANK_2015
    learn()


if __name__ == '__main__':
    main()


