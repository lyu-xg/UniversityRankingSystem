from alldata import dataset
from schoolname import affiliationName 
from evaluate import evalutate
from predictions import predictions
#from os.path import expanduser
from os import system

RelatedConferences = [
	['KDD','ICDM','CIKM','WWW','AAAI','ICDE'],
	['ICML','NIPS','AAAI','CVPR','KDD','ICASSP'],
	['SIGIR','CIKM','WWW','ECIR','WSDM','KDD'],
	['SIGMOD','ICDE','VLDB','CIKM','KDD','EDBT'],
	['SIGCOMM','INFOCOM','ICC','GLOBECOM','NSDI','IMC'],
	['MOBICOM','INFOCOM','ICC','GLOBECOM','SIGCOMM','MobiSys'],
	['FSE','ICSE','ASE','ISSTA','ICSM','MSR'],
	['MM','ICME','ICIP','CVPR','ICASSP','ICCV']]

topConferences = [entry[0] for entry in RelatedConferences]

schools = [key for key in affiliationName]
previousYears = ['2011','2012','2013','2014']
trainPath = 'svm_rank/train'
modelPath = 'svm_rank/model'
testPath = 'svm_rank/test'
predictionPath = 'svm_rank/prediction'

def generateData(writePath, yearRange, conference,qid):
	with open(writePath,'w') as outfile:
		for affiliationID in schools:
			futureYear = str(int(yearRange[-1])+1)
			futureYearFields = dataset[(affiliationID,conference,futureYear)]
			fieldSum = [0,0,0,0,0,0]
			for year in yearRange:
				# for loop averages all 3 year fields together
				fields = dataset[(affiliationID,conference,year)]
				# [f1, f2, f3, f4, f5, score]
				for index,value in enumerate(fields):
					fieldSum[index]+=value/len(yearRange)
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
	normalizeFactor = 20.0
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

def getEvaluation(conference):
	trueDict = addPositionToResult(getRealResult(2015,conference))
	rankingList = makeRankingList(predictions[conference])
	return evalutate(rankingList,trueDict)

def predictAndPrint():

	P = predictAllConference()
	print(P)
	for conference in P:
		print("\n\n***************"+conference+"*****************")
		printPredictionNicely(sortedItems(P[conference]))

if __name__ == "__main__":
	#predictAndPrint()	
	for conference in topConferences:
		print(conference,getEvaluation(conference))
	

