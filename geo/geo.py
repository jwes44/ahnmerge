import sys
import re
import sqlite3
from requests import get
from pprint import pprint
from json import dump
import csv 
import time

API_KEY = 'AIzaSyBIznSGVsF_Rj3Pz8meBgPyJ6voOPNUDeo'
def address_resolver(json):
    final = {}
    if json['results']:
        data = json['results'][0]
        for item in data['address_components']:
            for category in item['types']:
                data[category] = {}
                data[category] = item['long_name']
        final['street'] = data.get("route", None)
        final['state'] = data.get("administrative_area_level_1", None)
        final['city'] = data.get("locality", None)
        final['county'] = data.get("administrative_area_level_2", None)
        final['country'] = data.get("country", None)
        final['postal_code'] = data.get("postal_code", None)
        final['neighborhood'] = data.get("neighborhood",None)
        final['sublocality'] = data.get("sublocality", None)
        final['housenumber'] = data.get("housenumber", None)
        final['postal_town'] = data.get("postal_town", None)
        final['subpremise'] = data.get("subpremise", None)
        final['latitude'] = data.get("geometry", {}).get("location", {}).get("lat", None)
        final['longitude'] = data.get("geometry", {}).get("location", {}).get("lng", None)
        final['location_type'] = data.get("geometry", {}).get("location_type", None)
        final['postal_code_suffix'] = data.get("postal_code_suffix", None)
        final['street_number'] = data.get('street_number', None)
        final['formatted_address'] = data.get('formatted_address', None)
    return final
def get_address_details(address,):
    for i in range(5):
        try:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBIznSGVsF_Rj3Pz8meBgPyJ6voOPNUDeo' 
            url = url + '&address='+ address.replace(" ","+")
            response = get(url)
            data  = address_resolver(response.json())
            data['address'] = address
            return data
        except:
            pass
    return None

if __name__ == '__main__':
    """
    Provide the address via csv or paste it here 
    """
    pus = re.compile(r'\bUnited States of America\b',re.I)
    pus1 = re.compile(r'\bUnited States\b',re.I)
    psp = re.compile(r' *, *')
    conn = sqlite3.connect('c:/Users/j/ahnaddr1.db')
    conn.execute("CREATE TABLE IF NOT EXISTS addresses (adr_id INTEGER PRIMARY KEY, full_address STRING, city STRING, county STRING, state STRING, country STRING, latitude REAL, longitude REAL)")
    conn.execute("CREATE TABLE IF NOT EXISTS test_addresses (address STRING PRIMARY KEY NOT NULL, adr INTEGER REFERENCES addresses (adr_id)) WITHOUT ROWID")
    c = conn.cursor()
#    addresses = {}
#    address_to_search = ['Fayette County']
#    data = []
#    for i in address_to_search:
#        data.append(get_address_details(i))
    def fix_address(address):
        address = address.strip(', ')
        address = pus.sub('USA',address)
        address = pus1.sub('USA',address)
        address = psp.sub(', ',address)
        return address
    def check_address(addr):
        c.execute('SELECT country,state,county,city FROM test_addresses,addresses WHERE test_addresses.address=? AND test_addresses.adr = addresses.adr_id', [addr])
        ret = c.fetchall()
        if ret:
            if len(ret) ==  0:
                return None
            elif len(ret) ==  1:
                return ret[0]
        return None
#        return addr in addresses
insertsql = """INSERT INTO addresses(full_address,city,county,state,country,latitude,longitude) VALUES(?, ?, ?, ?, ?, ?, ?)"""
tcount = 0
ttries = 0
thits = 0
with open('C:/Users/j/ahnlst1.txt', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        tic = time.perf_counter()
        print(line,end=' ')
        with open(line, 'r', newline='', encoding='utf-8') as csvfile:
            line1 = line.replace('.csv','.csx')
            outfile = open(line1, 'w', newline='', encoding='utf-8')
            ahnreader = csv.reader(csvfile)
            ahnwriter = csv.writer(outfile)
            count = 0
            tries = 0
            hits = 0
            try:
                for row in ahnreader:
                    count = count+1
                    adx = [[],[]]
                    n=0
                    for i in [3,5]:
                        ad = row[i]
                        if ad:
                            ad = fix_address(ad)
        #                    print(row[0], row[3], '---', , '---', row[5], '---', fix_address(row[5]))
                            if ad:
                                add1 = check_address(ad)
                                tries = tries + 1
                                if not add1:
                                    try:
                                        address = get_address_details(ad)
                                        if 'formatted_address' in address:
#                                            c.execute("INSERT INTO addresses VALUES(?,?,?,?,?,?,?)", (address['formatted_address'],address['state'],address['city'],address['county'],address['country'],address['latitude'],address['longitude']) )
                                            c.execute(insertsql, (address['formatted_address'],address['city'],address['county'],address['state'],address['country'],address['latitude'],address['longitude']) )
                                            key = c.lastrowid
                                            c.execute("INSERT INTO test_addresses VALUES (?,?)", (ad, key))
                                            if ad != address['formatted_address']:
                                                c.execute("INSERT OR IGNORE INTO test_addresses VALUES (?,?)", (address['formatted_address'], key))
                                            conn.commit()
                                            adx[n].extend([address['country'],address['state'],address['county'],address['city']])
                                        else:
                                            tmp = ad.split(sep=',')
                                            tmp.reverse()
                                            addtmp = 4-len(tmp)
                                            for i in range(addtmp):
                                                tmp.append('')
                                            adx[n].extend(tmp)
                                    except sqlite3.Error as e:
                                        print(str(e))                                     
                                else:
                                    hits = hits + 1
                                    adx[n].extend(add1)
                        else:
                            adx[n] = ['','','','']
                        n = 1
                    outrow = row[0:3]
                    outrow.extend(adx[0])
                    outrow.append(row[4])
                    outrow.extend(adx[1])
                    outrow.extend(row[6:])
                    ahnwriter.writerow(outrow)
            except:
                print(sys.exc_info(), line, row)
        csvfile.close()
        outfile.close()
        toc = time.perf_counter()
        print(f" {count} lines, {hits} hits, {tries} tries, {toc - tic:0.4f} seconds")
        tcount = tcount + count
        ttries = ttries + tries
        thits = thits + hits
    f.close()
##     
#     
print(f" {tcount} lines, {thits} hits, {ttries} tries")
conn.commit()
conn.close()
#n = 0
#for a in addresses:
#    n = n + addresses[a]
#print(len(addresses), n)
# address_to_search = list(DictReader("path/to/csv/file"))
#    address_to_search = ['Fayette County']
#    data = []
#    for i in address_to_search:
#        data.append(get_address_details(i))
#   with open("data.csv",'w') as csvfile:
#       csvwriter = DictWriter(csvfile, fieldnames=data[0].keys(), quoting=QUOTE_ALL)
#       csvwriter.writeheader()
#       csvwriter.writerows(data)
