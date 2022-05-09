import sqlite3
import requests
import io
import zipfile
import time
#import pandas as pd
def loadtable(fi,tab,len):
    qm = '?'
    for n in range(1,len):
        qm = qm +',?'
    SQL = "INSERT INTO {} VALUES ({})".format(tab,qm)
#    print (SQL)
    for line in io.TextIOWrapper(fi, encoding='utf-8'):
        line = line.strip('\n')
        row = line.split('\t')
        conn.execute(SQL, row)

files = (('http://download.geonames.org/export/dump/admin1CodesASCII.txt','admin1CodesASCII',4),
         ('http://download.geonames.org/export/dump/admin2Codes.txt','admin2Codes',4),
         ('http://download.geonames.org/export/dump/allCountries.zip','geonames',19),
         ('http://download.geonames.org/export/dump/alternateNamesV2.zip','alternateNamesV2',10))
conn = sqlite3.connect(':memory:')
f = open('E:\geonames2.db.sql','rt', encoding='utf-8')
s = f.read()
f.close()
conn.executescript(s)
tic = time.perf_counter()
f = open('C:/Users/j/Downloads/ISO_3166_country_codes.txt','rb')
loadtable(f,'ISO_3166_country_codes',5)
toc = time.perf_counter()
f.close()
print(f" insert from C:/Users/j/Downloads/ISO_3166_country_codes.txt {toc - tic:0.4f} seconds")
for i in files:
    fn = i[0]
    tic = time.perf_counter()
    remotefile = requests.get(fn)
    toc = time.perf_counter()
    print(f"download {fn} {toc - tic:0.4f} seconds")
    if '.zip' in fn:
        root = zipfile.ZipFile(io.BytesIO(remotefile.content))
        for name in root.namelist():
            if 'readme' not in name and 'iso-' not in name:
                tic = time.perf_counter()
                f = root.open(name)
                loadtable(f,i[1],i[2])
                f.close()
                toc = time.perf_counter()
                print(f" insert from {name} {toc - tic:0.4f} seconds")
    else:
#        f = open(fn,'rt', encoding='utf-8')
        tic = time.perf_counter()
        loadtable(io.BytesIO(remotefile.content),i[1],i[2])
        toc = time.perf_counter()
        print(f" insert from {fn} {toc - tic:0.4f} seconds")
#        f.close()
    conn.commit()
tic = time.perf_counter()
conn.execute('CREATE INDEX IF NOT EXISTS "geoix" ON "geonames" ("geonameid")')
conn.execute('CREATE INDEX IF NOT EXISTS "altix" ON "alternateNamesV2" ("alternatename" COLLATE NOCASE)')
conn.execute('CREATE INDEX IF NOT EXISTS "gnix" ON "geonames" ("name" COLLATE NOCASE)')
conn.execute('CREATE INDEX IF NOT EXISTS "ganix" ON "geonames" ("asciiname" COLLATE NOCASE)')
conn.execute('CREATE INDEX IF NOT EXISTS "ad1ix" ON "admin1CodesASCII" ("code")')
conn.execute('CREATE INDEX IF NOT EXISTS "ad2ix" ON "admin2Codes" ("codes")')
conn.execute('CREATE INDEX IF NOT EXISTS "ccix" ON "ISO_3166_country_codes" ("Alpha2code")')
conn.commit()
toc = time.perf_counter()
print(f" Create indices {toc - tic:0.4f} seconds")
tic = time.perf_counter()
dest = sqlite3.connect('e:/geonames.db')
conn.backup(dest)
dest.close()
conn.close()
toc = time.perf_counter()
print(f" Copy and close {toc - tic:0.4f} seconds")
