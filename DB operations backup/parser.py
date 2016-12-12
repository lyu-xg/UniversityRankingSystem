'''
EAMPLE
def filter(txt, oldfile, newfile):

    Read a list of names from a file line by line into an output file.
    If a line begins with a particular name, insert a string of text
    after the name before appending the line to the output file.


    with open(newfile, 'w') as outfile, open(oldfile, 'r', encoding='utf-8') as infile:
        for line in infile:
            if line.startswith(txt):
                line = line[0:len(txt)] + ' - Truly a great person!\n'
            outfile.write(line)

# input the name you want to check against
text = input('Please enter the name of a great person: ')
letsgo = filter(text,'Spanish', 'Spanish2')
'''
from os.path import expanduser
import sqlite3

sqlite_file = expanduser("~") + "/data/db.sqlite"

SelectedAffiliationsPath = expanduser("~") + "/data/2016KDDCupSelectedAffiliations.txt"
SelectedPapersPath = expanduser("~") + "/data/2016KDDCupSelectedPapers.txt"
AuthorsPath = expanduser("~") +  "/data/Authors.txt"
PaperAuthorAffiliationsPath = expanduser("~") +  "/data/PaperAuthorAffiliations.txt"
PaperReferencesPath = expanduser("~") + "/data/PaperReferences.txt"
ShangHaiRankingPath = expanduser("~") + "/Desktop/shanghaiData.csv"
FieldOfStudyHierarchyPath = expanduser("~") + "/data/Papers.txt"
#dataPath = expanduser("~") + "/data/Papers.txt"

if __name__ == "__main__":
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()

    '''
    with open(FieldOfStudyHierarchyPath) as file:
        for index,line in enumerate(file):
            fields = line.strip("\n").strip("\r").replace("'","''").split("\t")
            #print(fields)
            assert(len(fields)==11)
            if index%100000==0:
                print("processing: no. "+str(index))
            sql = "INSERT INTO Papers (PaperID,Year,DOI,ConferenceID,PaperRank) VALUES ('{}','{}','{}','{}','{}')".format(fields[0],fields[3],fields[5],fields[9],fields[10])
            #sql = "UPDATE SelectedAffiliations SET AffiliationName = '{}' WHERE AffiliationID = '{}'".format(fields[1],fields[0])
            #print(sql)
            cursor.execute(sql)
    '''
    with open('temp') as infile:
        for line in infile:
            sql = line.strip('\n')
            cursor.execute(sql) 
    connection.commit()
    connection.close()
