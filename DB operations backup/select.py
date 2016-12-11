from os.path import expanduser
import sqlite3
sqlite_file = expanduser("~") + "/data/db.sqlite"

connection = sqlite3.connect(sqlite_file)
cursor = connection.cursor()


PossibleConferences = [
	['KDD','ICDM','CIKM','WWW','AAAI','ICDE'],
	['ICML','NIPS','AAAI','CVPR','KDD','ICASSP'],
	['SIGIR','CIKM','WWW','ECIR','WSDM','KDD'],
	['SIGMOD','ICDE','VLDB','CIKM','KDD','EDBT'],
	['SIGCOMM','INFOCOM','ICC','GLOBECOM','NSDI','IMC'],
	['MOBICOM','INFOCOM','ICC','GLOBECOM','SIGCOMM','MobiSys'],
	['FSE','ICSE','ASE','ISSTA','ICSM','MSR'],
	['MM','ICME','ICIP','CVPR','ICASSP','ICCV']]

# After Flaten:
PossibleConferencesList = ['KDD', 'ICDM', 'CIKM', 'WWW', 'AAAI', 'ICDE', 'ICML', 'NIPS', 'AAAI', 'CVPR', 'KDD', 'ICASSP', 'SIGIR', 'CIKM', 'WWW', 'ECIR', 'WSDM', 'KDD', 'SIGMOD', 'ICDE', 'VLDB', 'CIKM', 'KDD', 'EDBT', 'SIGCOMM', 'INFOCOM', 'ICC', 'GLOBECOM', 'NSDI', 'IMC', 'MOBICOM', 'INFOCOM', 'ICC', 'GLOBECOM', 'SIGCOMM', 'MobiSys', 'FSE', 'ICSE', 'ASE', 'ISSTA', 'ICSM', 'MSR', 'MM', 'ICME', 'ICIP', 'CVPR', 'ICASSP', 'ICCV']
ConferenceSet = set(PossibleConferencesList)
ConferenceNameToID = {'NSDI': '450B3A86', 'FSE': '477F6C83', 'INFOCOM': '442BD7CD', 'MSR': '454AACD8', 'ICSE': '45FFFB88', 'ICSM': '4532399F', 'AAAI': '46A05BB0', 'ISSTA': '430D9705', 'ICDE': '45610CDA', 'KDD': '436976F3', 'GLOBECOM': '43701CEE', 'ICML': '465F7C62', 'ICDM': '468A7487', 'CVPR': '45083D2F', 'SIGIR': '43FD776C', 'MobiSys': '469BDC4B', 'ASE': '45878F67', 'ICASSP': '42D493FC', 'EDBT': '43820346', 'IMC': '452D6964', 'SIGCOMM': '44B13001', 'SIGMOD': '460A7036', 'ICC': '436150FA', 'VLDB': '4390334E', 'ICME': '432251B5', 'MOBICOM': '42F4F2CC', 'ICIP': '455477A7', 'WSDM': '42C7B402', 'WWW': '43ABF249', 'ECIR': '465D33C1', 'MM': '43AA5802', 'CIKM': '472C6E2D', 'ICCV': '45701BF3', 'NIPS': '43319DD4'}
ConferenceIDs = set(['42F4F2CC', '45610CDA', '465D33C1', '43FD776C', '46A05BB0', '45083D2F', '460A7036', '472C6E2D', '436150FA', '468A7487', '450B3A86', '454AACD8', '43701CEE', '42D493FC', '43ABF249', '43AA5802', '45878F67', '45701BF3', '43319DD4', '45FFFB88', '43820346', '432251B5', '430D9705', '42C7B402', '477F6C83', '4390334E', '455477A7', '442BD7CD', '4532399F', '452D6964', '44B13001', '469BDC4B', '436976F3', '465F7C62'])

FeatureSpace = {}
'''
cursor.execute('select distinct NormalizedAffiliationName')
for entry in cursor.fetchall():
	fields = [str(i) for i in entry]

with open('temp','w') as outfile:

	insertCount = 0
	print('starting')
	for index,entry in enumerate(cursor.execute('select * from PaperAuthorAffiliations')):
		fields = [str(i.encode('utf-8')) if isinstance(i, unicode) else i for i in entry]
		# id, paperID, AuthorID, AffiliationID, OrName, NormalName, AuthorSQ
		#print(entry)
		#print(fields[6],fields[3])
		if int(fields[6]) in [1,2,3,4,5,6] and fields[3] in affiliationIDs: 
			#FeatureSpace[fields[1]]=fields[0]
			sql = "INSERT INTO UsefulAAA (PaperID, AuthorID, AffiliationID, AuthorSequence) VALUES ('{}','{}','{}','{}')".format(fields[1],fields[2],fields[3],int(fields[6]))
			insertCount += 1
			if index%1000000==0:
				print("inserting: no. "+str(insertCount)+" out of "+str(index))
			#cursor.execute(sql)
			outfile.write(sql+'\n')
'''
connection.commit()
connection.close()
