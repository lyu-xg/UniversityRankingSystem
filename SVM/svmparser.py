from alldata import dataset
from schoolname import affiliationName 
from evaluate import evalutate
from predictions import rPredictions
from predictions import svmpredictions
#from os.path import expanduser
from os import system

RelatedConferences = {
	'KDD':['ICDM','CIKM','WWW','AAAI','ICDE'],
	'ICML':['NIPS','AAAI','CVPR','KDD','ICASSP'],
	'SIGIR':['CIKM','WWW','ECIR','WSDM','KDD'],
	'SIGMOD':['ICDE','VLDB','CIKM','KDD','EDBT'],
	'SIGCOMM':['INFOCOM','ICC','GLOBECOM','NSDI','IMC'],
	'MOBICOM':['INFOCOM','ICC','GLOBECOM','SIGCOMM','MobiSys'],
	'FSE':['ICSE','ASE','ISSTA','ICSM','MSR'],
	'MM':['ICME','ICIP','CVPR','ICASSP','ICCV']}

topConferences = ['ICML','KDD',  'SIGIR', 'SIGMOD', 'SIGCOMM', 'MOBICOM', 'FSE', 'MM']


schools = [key for key in affiliationName]
previousYears = ['2011','2012','2013','2014']
trainPath = 'svm_rank/train'
modelPath = 'svm_rank/model'
testPath = 'svm_rank/test'
predictionPath = 'svm_rank/prediction'

def generateData(writePath, yearRange, conference,qid):
	similarConferences = []
	with open(writePath,'w') as outfile:
		for affiliationID in schools:
			futureYear = str(int(yearRange[-1])+1)
			futureYearFields = dataset[(affiliationID,conference,futureYear)]
			fieldSum = [0,0,0,0,0,0]
			for year in yearRange:

				for conf in RelatedConferences[conference]+[conference]:
					fields = dataset[(affiliationID,conf,year)]
					for index,value in enumerate(fields):
						fieldSum[index]+=value/6

			line = "{} qid:{} 1:{} 2:{} 3:{} 4:{} 5:{}\n".format(futureYearFields[-1],qid,fieldSum[0],fieldSum[1],fieldSum[2],fieldSum[3],fieldSum[4])
			outfile.write(line)


def getSchoolName(schoolIndex):
	schoolID = schools[schoolIndex]
	return affiliationName[schoolID]

def sortedItems(inDict):
	return sorted(inDict.items(), key=lambda x: x[1])

def readPrediction():
	result = {}
	with open(predictionPath) as infile:
		for index,line in enumerate(infile):
			#print(index,line)
			schoolName = getSchoolName(index)
			result[schoolName] = (float(line.strip('\n')))
	return result

def generateTrainAndTestData(conference):
	generateData(trainPath,['2011','2012','2013'],conference,1)
	generateData(testPath,['2012','2013','2014'],conference,2)

def getRealResult(year,conference):
	year = str(year)
	result = {}
	for affiliationID in schools:
		fields = dataset[(affiliationID,conference,year)]
		result[affiliationName[affiliationID]] = fields[-1]
	return result

def printPredictionNicely(inList):
	inList.reverse()
	for school,score in inList:
		if score==0:
			break
		print(school,score)

def predictAllConference():
	results = {}
	for conference in topConferences:
		generateTrainAndTestData(conference)
		runModelandPredict()
		prediction = readPrediction()
		results[conference]=prediction
	return results

def runModelandPredict():
	normalizeFactor = 10.0
	system("svm_rank/./svm_rank_learn -c {} {} {}".format(normalizeFactor,trainPath,modelPath))
	system("svm_rank/./svm_rank_classify {} {} {}".format(testPath,modelPath,predictionPath))


def makeRankingList(inDict):
	sortedPair = sortedItems(inDict)
	sortedPair.reverse()
	return [school for school,score in sortedPair]

def addPositionToResult(inDict):
	sortedPair = sortedItems(inDict)
	sortedPair.reverse()
	result = {}
	for index,(school,score) in enumerate(sortedPair):
		if index == 20:
			break
		result[school] = (score,index+1)
	return result

def getEvaluation(conference,predictions):
	trueDict = addPositionToResult(getRealResult(2015,conference))
	rankingList = makeRankingList(predictions[conference])
	return evalutate(rankingList,trueDict)

def predictAndPrint():
	P = predictAllConference()
	print(P)
	for conference in P:
		print("\n\n***************"+conference+"*****************")
		printPredictionNicely(sortedItems(P[conference]))
	return P

def getRegressionPredictionAndRank():
	result = {}
	# result['KDD'] -> ['CMU':745, 'NEU':744 ...]
	for conference in topConferences:
		temp = {}
		ranking = rPredictions[conference]
		ranking.reverse()
		for index,affiliationID in enumerate(ranking):
			temp[affiliationName[affiliationID]] = index+1
		result[conference] = temp
	return result

def getSVMPredictionAndRank():
	result={}
	for conference in topConferences:
		ranking = sortedItems(svmpredictions[conference])
		temp = {}
		for index,(school,score) in enumerate(ranking):
			temp[school] = index + 1
		result[conference] = temp
	return result

def ensembleRanking():
	result1 = getRegressionPredictionAndRank()
	result2 = getSVMPredictionAndRank()
	result = {}
	for conference in topConferences:
		rank1 = result1[conference]
		rank2 = result2[conference]
		temp = {}
		for affiliationID in schools:
			school = affiliationName[affiliationID]
			temp[school] = rank1[school]+rank2[school]
		result[conference] = temp
	return result

if __name__ == "__main__":
	'''
	predictions = predictAndPrint()
	for conference in topConferences:
		print(conference,getEvaluation(conference,predictions))
	'''
	#for conference in topConferences:
	#print('ICML',getEvaluation('ICML',ensembleRanking()))
	print('MM',getEvaluation('MM',ensembleRanking()))
	
	#printPredictionNicely(sortedItems(ensembleRanking()['ICML']))
