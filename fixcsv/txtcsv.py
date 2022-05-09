import re
import csv
import os
import sys

txt = set()
with open('C:/Users/j/Google Drive/temp/ahn1.lst') as f:
    for le in f:
        le = le.strip()
        rn = le.rsplit('\\',1)[1]
        rn = rn.split('.')[0]
        txt.add(rn.lower())
for x in os.listdir('C:/Users/j/ahnp'):
    if x.endswith('.csv'):
        le = x.strip()
        rn = le.split('.csv')[0]
        if not rn.lower() in txt:
            print(x)
#print(sorted(txt))
