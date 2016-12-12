from os.path import expanduser
import sqlite3
from schoolname import affiliationName
sqlite_file = expanduser("~") + "/data/db.sqlite"

if __name__ == "__main__":
	connection = sqlite3.connect(sqlite_file)
	cursor = connection.cursor()

	'''
	result = {}
	
	
	for entry in cursor.execute('select * from SelectedAffiliations'):
		fields = [str(i.encode('utf-8')) if isinstance(i, unicode) else i for i in entry]
		result[=fields[1]]=fields[2]
	print(result)

	'''
	with open('temp','w') as outfile:

		insertCount = 0
		print('starting')
		for index,entry in enumerate(cursor.execute('select * from PaperAuthorAffiliations')):
			fields = [str(i.encode('utf-8')) if isinstance(i, unicode) else i for i in entry]
			# id, paperID, AuthorID, AffiliationID, OrName, NormalName, AuthorSQ
			#print(entry)
			#print(fields[6],fields[3])
			if int(fields[6]) in [1,2,3,4,5,6] and fields[3] in affiliationName: 
				#FeatureSpace[fields[1]]=fields[0]
				sql = "INSERT INTO NewUsefulAAA (PaperID, AuthorID, AffiliationID, AuthorSequence) VALUES ('{}','{}','{}','{}')".format(fields[1],fields[2],fields[3],int(fields[6]))
				insertCount += 1
				#cursor.execute(sql)
				outfile.write(sql+'\n')
			if index%1000000==0:
					print("inserting: no. "+str(insertCount)+" out of "+str(index))
	
	connection.commit()
	connection.close()
