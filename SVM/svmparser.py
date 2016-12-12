from alldata import dataset
from schoolname import affiliationName 
from os.path import expanduser
from os import system

PossibleConferences = [
	['KDD','ICDM','CIKM','WWW','AAAI','ICDE'],
	['ICML','NIPS','AAAI','CVPR','KDD','ICASSP'],
	['SIGIR','CIKM','WWW','ECIR','WSDM','KDD'],
	['SIGMOD','ICDE','VLDB','CIKM','KDD','EDBT'],
	['SIGCOMM','INFOCOM','ICC','GLOBECOM','NSDI','IMC'],
	['MOBICOM','INFOCOM','ICC','GLOBECOM','SIGCOMM','MobiSys'],
	['FSE','ICSE','ASE','ISSTA','ICSM','MSR'],
	['MM','ICME','ICIP','CVPR','ICASSP','ICCV']]

topConferences = [entry[0] for entry in PossibleConferences]

schools = [key for key in affiliationName]
previousYears = ['2011','2012','2013','2014']
trainPath = 'svm_rank/train'
modelPath = 'svm_rank/model'
testPath = 'svm_rank/test'
predictionPath = 'svm_rank/prediction'

def generateData(writePath, yearRange, conference,qid):
	with open(writePath,'w') as outfile:
		for year in yearRange:
			qid += 1
			for affiliationID in schools:
				fields = dataset[(affiliationID,conference,year)]
				# [f1, f2, f3, f4, f5, score]
				line = "{} qid:{} 1:{} 2:{} 3:{} 4:{} 5:{}\n".format(fields[-1],qid,fields[0],fields[1],fields[2],fields[3],fields[4])
				outfile.write(line)
	return qid

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
	qid=generateData(trainPath,previousYears,conference,0)
	generateData(testPath,['2015'],conference,qid)

def getResult(year,conference):
	year = str(year)
	result = {}
	for affiliationID in schools:
		fields = dataset[(affiliationID,conference,year)]
		result[affiliationName[affiliationID]] = fields[-1]
	return sortedItems(result)

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
	runModel()
	runPrediction()

def runModel():
	normalizeFactor = 10.0
	system("svm_rank/./svm_rank_learn -c {} {} {}".format(normalizeFactor,trainPath,modelPath))

def runPrediction():
	system("svm_rank/./svm_rank_classify {} {} {}".format(testPath,modelPath,predictionPath))

if __name__ == "__main__":
	#generateTrainAndTestData('KDD')
	#printPredictionNicely(getResult(2015,'KDD'))
	P = predictAllConference()
	print(P)
	for conference in P:
		print("\n\n***************"+conference+"*****************")
		printPredictionNicely(sortedItems(P[conference]))
