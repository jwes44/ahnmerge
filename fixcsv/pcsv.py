import re
import csv
import os
import sys

n=0
age = 0
nm=0
mage = 0
nf=0
fage = 0
for x in os.listdir('C:/Users/j/ahn'):
    if x.endswith('.csv'):
        with open('C:/Users/j/ahn/'+x, newline='', encoding='utf-8') as csvfile:
            ahnreader = csv.reader(csvfile) 
            rows = {}
            try:
                for row in ahnreader:
                    r0 = int(row[0].split('.')[0])
                    rows[r0] = row
                    try:
                        if row[4].isdecimal() and row[6].isdecimal():
                            age = age + int(row[6]) - int(row[4])
                            n = n + 1
                    except:
                        print("err",x,row)
                    if row[4].isdecimal():
                        if r0//2 in rows:
                            t = rows[r0//2][4]
                            if t.isdecimal():
                                if r0%2:
                                    fage = fage + int(t) - int(row[4])
                                    nf = nf + 1
                                else:
                                    mage = mage + int(t) - int(row[4])
                                    nm = nm + 1
            except:
                print("err", sys.exc_info()[0],x,row)
print("av",age/n)
print("m",mage/nm)
print("f",fage/nf)

