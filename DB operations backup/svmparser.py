from alldata import dataset
from schoolname import affiliationName 
from os.path import expanduser

schools = affiliationName.keys()
previousYears = ['2011','2012','2013','2014']
trainPath = expanduser('~')+'/Desktop/svm_light/train'
testPath = expanduser('~') + '/Desktop/svm_light/test'
predictionPath = expanduser('~')+'/Desktop/svm_light/prediction'

def generateData(writePath, yearRange, conference):
	qid = 0
	with open(writePath,'w') as outfile:
		for year in yearRange:
			qid += 1
			for affiliationID in schools:
				fields = dataset[(affiliationID,conference,year)]
				# [f1, f2, f3, f4, f5, score]
				line = "{} qid:{} 1:{} 2:{} 3:{} 4:{} 5:{}\n".format(fields[-1],qid,fields[0],fields[1],fields[2],fields[3],fields[4])
				outfile.write(line)

def getSchoolName(schoolIndex):
	schoolID = schools[schoolIndex]
	return affiliationName[schoolID]

def readResult(readPath):
	result = {}
	with open(readPath) as infile:
		for index,line in enumerate(infile):
			print(index,line)
			schoolName = getSchoolName(index)
			result[schoolName] = (float(line.strip('\n')))
	return result

if __name__ == "__main__":
	#generateData(trainPath,previousYears,'KDD')
	#generateData(testPath,['2015'],'KDD')
	print readResult(predictionPath)
	#print len(schools)