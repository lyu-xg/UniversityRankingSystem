import sqlite3
from os.path import expanduser
from schoolname import affiliationName
PossibleConferencesList = ['KDD', 'ICDM', 'CIKM', 'WWW', 'AAAI', 'ICDE', 'ICML', 'NIPS', 'AAAI', 'CVPR', 'KDD', 'ICASSP', 'SIGIR', 'CIKM', 'WWW', 'ECIR', 'WSDM', 'KDD', 'SIGMOD', 'ICDE', 'VLDB', 'CIKM', 'KDD', 'EDBT', 'SIGCOMM', 'INFOCOM', 'ICC', 'GLOBECOM', 'NSDI', 'IMC', 'MOBICOM', 'INFOCOM', 'ICC', 'GLOBECOM', 'SIGCOMM', 'MobiSys', 'FSE', 'ICSE', 'ASE', 'ISSTA', 'ICSM', 'MSR', 'MM', 'ICME', 'ICIP', 'CVPR', 'ICASSP', 'ICCV']

import numpy as np
def paperNumber(workset):
	# number of distinct papers
	papers = [entry[0] for entry in workset]
	#print(len(set(papers)))
	return len(set(papers))

def authorNumber(workset):
	# number of author who published at least one paper this year
	authors = [entry[2] for entry in workset]
	return len(set(authors))

def authorPaperPair(workset):
	# number of (author,paper) pair
	return len(workset)

def firstAuthor(workset):
	firstAuthors = [entry[4] for entry in workset if entry[4] == 1]
	return len(firstAuthors)

def secondAuthor(workset):
	secondAuthors = [entry[4] for entry in workset if entry[4] > 1]
	return len(secondAuthors)

def score(workset,cursor):
	s = 0
	for entry in workset:
		s += 1.0/getNumOfThisPaper(entry[0],cursor)
	#if s>0:
		#print(s)
	return s

def getNumOfThisPaper(paperID,cursor):
	cursor.execute("select COUNT(*) from Final where PaperID ='{}'".format(paperID))
	return cursor.fetchone()[0]
	#return len(filter((lambda entry: entry[0]==paperID),table))

sqlite_file = expanduser("~") + "/data/db.sqlite"

if __name__ == "__main__":
	connection = sqlite3.connect(sqlite_file)
	cursor = connection.cursor()

	dataSet = {}

	table = []
	for entry in cursor.execute("select PaperID,Year,AuthorID,AffiliationID,AuthorSequence,ConferenceShortName from Final"):
	    table.append([str(i.encode('utf-8')) if isinstance(i, unicode) else i for i in entry])
	print('get table')
	print(len(table))

	for school in affiliationName.keys():
		schoolworkset = filter((lambda entry: entry[3]==school),table)
		for year in ['2011','2012','2013','2014','2015']:
			yearworkset = filter((lambda entry: entry[1]==year),schoolworkset)
			# all entry that is of this school and this year on KDD
			for conference in PossibleConferencesList:
				workset = filter((lambda entry: entry[5]==conference),yearworkset)
				dataSet[(school,conference,year)] =  [
					paperNumber(workset),
					authorNumber(workset),
					authorPaperPair(workset),
					firstAuthor(workset),
					secondAuthor(workset),
					score(workset,cursor)]


	print(dataSet)
	np.save('data.npy',dataSet)

	connection.commit()
	connection.close()
