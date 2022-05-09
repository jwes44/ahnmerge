import re
import csv
import os
import sys

txt = set()
with open('C:/Users/j/Google Drive/temp/ahn.lst.sav') as f:
    for le in f:
        le = le.strip()
        rn = le.rsplit('/',1)[1]
        rn = rn.split('.txt')[0]
        txt.add(rn.lower())
for x in os.listdir('C:/Users/j/temp'):
    if x.endswith('.txt'):
        le = x.strip()
        rn = le.split('.txt')[0]
        if not rn.lower() in txt:
            print(x)
#print(sorted(txt))
