import sqlite3
from os.path import expanduser
from select import affiliationIDs

sqlite_file = expanduser("~") + "/data/db.sqlite"
connection = sqlite3.connect(sqlite_file)
cursor = connection.cursor()

dataSet = {}

table = []
for entry in cursor.execute('select PaperID,Year,AuthorID,AffiliationID,AuthorSequence from KDDFinal'):
    table.append([str(i.encode('utf-8')) if isinstance(i, unicode) else i for i in entry])
print('get table')
print(len(table))
def paperNumber(workset):
	# number of distinct papers
	papers = [entry[0] for entry in workset]
	print(len(set(papers)))
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

def score(workset):
	s = 0
	for entry in workset:
		s += 1/getNumOfThisPaper(entry[0])
	return s

def getNumOfThisPaper(paperID):
	cursor.execute("select COUNT(*) from Final where PaperID ='{}'".format(paperID))
	return cursor.fetchone()[0]

for school in affiliationIDs:
	for year in ['2011','2012','2013','2014']:
		workset = filter((lambda entry: entry[1]==year and entry[3]==school),table)
		# all entry that is of this school and this year on KDD
		dataSet[(school,'KDD',year)] =  [
			paperNumber(workset),
			authorNumber(workset),
			authorPaperPair(workset),
			firstAuthor(workset),
			secondAuthor(workset),
			score(workset)]



print(dataSet)

connection.commit()
connection.close()
