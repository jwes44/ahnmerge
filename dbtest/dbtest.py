import sqlite3
conn = sqlite3.connect('c:/Users/j/dbtest.db')
#conn.execute("""CREATE TABLE dbtest (
#	geonameid	INTEGER,
#	name	TEXT,
#	asciiname	TEXT,
#	latitude	REAL,
#	longitude	REAL,
#	featureclass	TEXT,
#	featurecode	TEXT,
#	countrycode	TEXT,
#	cc2	TEXT,
#	admin1code	INTEGER,
#	admin2code	TEXT,
#	admin3code	TEXT,
#	admin4code	TEXT)"""
#)
with open('C:/Users/j/geo1.txt', encoding='utf-8') as f:
    rn = 0
    for line in f:
        line = line.strip('\n')
        row = line.split('\t')
        conn.execute("INSERT INTO dbtest VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
        rn = rn + 1
    f.close()
conn.commit()
conn.close()
