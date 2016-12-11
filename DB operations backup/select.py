from os.path import expanduser
import sqlite3
sqlite_file = expanduser("~") + "/data/db.sqlite"

if __name__ == "__main__":
	connection = sqlite3.connect(sqlite_file)
	cursor = connection.cursor()



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
