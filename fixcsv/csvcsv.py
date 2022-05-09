import re
import csv
import os
import sys

txt = set()
for x in os.listdir('C:/Users/j/ahn'):
    if x.endswith('.csv'):
        le = x.strip()
        rn = le.split('.csv')[0]
        txt.add(rn.lower())
for x in os.listdir('C:/Users/j/ahnp'):
    if x.endswith('.csv'):
        le = x.strip()
        rn = le.split('.csv')[0]
        if rn.lower() in txt:
            print(x)
#print(sorted(txt))
