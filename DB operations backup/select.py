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

#sql = "CREATE TABLE UsefulConferences (ConferenceID TEXT, ConferenceShortName TEXT)"
# Creating a new SQLite table
#cursor.execute(sql)

cursor.execute('select * from Conferences')
for entry in cursor.fetchall():
	fields = [str(i) for i in entry]
	if fields[1] in ConferenceSet:
		sql = "INSERT INTO UsefulConferences (ConferenceID,ConferenceShortName) VALUES ('{}','{}')".format(fields[0],fields[1])
		print(sql)
		cursor.execute(sql)
connection.commit()
connection.close()
