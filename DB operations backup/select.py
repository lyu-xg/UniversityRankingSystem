from os.path import expanduser
import sqlite3
sqlite_file = expanduser("~") + "/data/db.sqlite"

connection = sqlite3.connect(sqlite_file)
cursor = connection.cursor()



cursor.execute('select * from SelectedAffiliations')
for records in cursor.fetchall():
  print(records)
connection.close()
