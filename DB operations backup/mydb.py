# only used to create tables
import sqlite3
from os.path import expanduser

sqlite_file = expanduser("~") + "/data/db.sqlite"

if __name__ == "__main__":
	connection = sqlite3.connect(sqlite_file)
	cursor = connection.cursor()
	#sql = "CREATE TABLE SelectedAffiliations (id INTEGER PRIMARY KEY AUTOINCREMENT, AffiliationID TEXT, AffiliationName TEXT)"
	sql = "CREATE TABLE NewUsefulAAA (PaperID TEXT, AuthorID TEXT, AffiliationID TEXT, AuthorSequence INT)"
	# Creating a new SQLite table
	cursor.execute(sql)
	# Committing changes and closing the connection to the database file
	connection.commit()
	connection.close()

