import re
import csv
import os
import sys

def bd(p,d):
    if p and d:
        return '{}, {}'.format(p,d)
    else:
        return '{}{}'.format(p,d)
txt = set()
tx1 = set()
dir1 = 'C:/Users/j/Google Drive/temp'
dir2 = 'C:/Users/j/ahnp'
p1 = re.compile(r'\. ')
for x in os.listdir(dir1):
    if x.endswith('.txt'):
        le = x.strip()
        rn = le.split('.txt')[0]
        txt.add(rn.lower())
for x in os.listdir(dir2):
    if x.endswith('.csv'):
        le = x.strip()
        rn = le.split('.csv')[0]
        if rn.lower() in txt:
            tx1.add(rn.lower())
for i in sorted(tx1):
    tx = set()
    tfn = dir1 + '/' + i + '.txt'
    print(tfn)
    with open(tfn, encoding='utf-8') as f:
        for le in f:
            b1=p1.split(le)   # split number from name
            tx.add(int(b1[0]))
    fn = dir2 + '/' + i + '.csv'
    with open(fn, newline='', encoding='utf-8') as csvfile:
        ahnreader = csv.reader(csvfile) 
        for row in ahnreader:
            if int(row[0].strip('.')) not in tx:
                born = bd(row[3], row[4])
                died = bd(row[5], row[6])
                ah = '{}. {} {} born: {} died: {}'.format(row[0], row[1], row[2].title(), born, died)
                print(ah)
            ll = row
