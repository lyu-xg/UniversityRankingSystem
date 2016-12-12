from math import log
def evalutate(predictRank,trueDic):
    #
    #   rank is the predict rank, should contain all affiliation
    #   Example: ['09E3EE34', '012E6F4E', '4CE6FC2D', '00FF56A8', '0489A984', '05E79D01', .....]
    #   dic is true scores and it's true rank position.
    #       key : affiliationID, value:(score,rank)
    #   Example: {'0B845BA3': (7.249999999999999, 2), '00FF56A8': (5.633333333333334, 6),...}

    DCG = 0.0
    IDCG = 0.0

    for school in trueDic:
        IDCG += trueDic[school][0]/(log(trueDic[school][1]+1)/log(2))

    for school in trueDic:
        predict_rank = predictRank.index(school) + 1
        DCG += trueDic[school][0]/(log(predict_rank+1)/log(2))

    NDCG = DCG/IDCG

    return NDCG
