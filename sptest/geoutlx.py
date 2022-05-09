import sqlite3
import re

source = sqlite3.connect('e:/geonames.db')
conn = sqlite3.connect(':memory:')
source.backup(conn)
#conn = sqlite3.connect('e:/geonames.db')
c = conn.cursor()
abbs = {
'Ala.' : 'Alabama',
'Ariz.' : 'Arizona',
'Ark.' : 'Arkansas',
'Calif.' : 'California',
'Colo.' : 'Colorado',
'Conn.' : 'Connecticut',
'Del.' : 'Delaware',
'D.C.' : 'District of Columbia',
'Fla.' : 'Florida',
'Ga.' : 'Georgia',
'Ill.' : 'Illinois',
'Ind.' : 'Indiana',
'Kan.' : 'Kansas',
'Kans.' : 'Kansas',
'Ky.' : 'Kentucky',
'La.' : 'Louisiana',
'Md.' : 'Maryland',
'Mass.' : 'Massachusetts',
'Mich.' : 'Michigan',
'Minn.' : 'Minnesota',
'Miss.' : 'Mississippi',
'Mo.' : 'Missouri',
'Mont.' : 'Montana',
'Neb.' : 'Nebraska',
'Nebr.' : 'Nebraska',
'Nev.' : 'Nevada',
'N.H.' : 'New Hampshire',
'N.J.' : 'New Jersey',
'N.M.' : 'New Mexico',
'N. Mex.' : 'New Mexico',
'N.Y.' : 'New York',
'N.C.' : 'North Carolina',
'N.D.' : 'North Dakota',
'N. Dak.' : 'North Dakota',
'Okla.' : 'Oklahoma',
'Ore.' : 'Oregon',
'Oreg.' : 'Oregon',
'Pa.' : 'Pennsylvania',
'PQ' : 'Québec',
'R.I.' : 'Rhode Island',
'S.C.' : 'South Carolina',
'S.D.' : 'South Dakota',
'S. Dak.' : 'South Dakota',
'St' : 'Saint',
'St.' : 'Saint',
'Ste' : 'Sainte',
'Ste.' : 'Sainte',
'Tenn.' : 'Tennessee',
'Tex.' : 'Texas',
'Vt.' : 'Vermont',
'Va.' : 'Virginia',
'Wash.' : 'Washington',
'W. Va.' : 'West Virginia',
'Wis.' : 'Wisconsin',
'Wyo.' : 'Wyoming'
}

def valname(address):
    def name_format(t):
        n = t.name
        if t.num == 4:
            n = n + (', ' + t.adm2 if t.adm2 else '') + (', ' + t.adm1 if t.adm1 else '') + (', ' + t.country if t.country else '')
        elif t.num == 3:
            n = n + (', ' + t.adm1) if t.adm1 else '' + (', ' + t.country) if t.country else ''
        elif t.num == 2:
            n = n + (', ' + t.country) if t.country else ''
        return n
    def fixadd(a):
        a = a.replace('...','%')
        b = re.split('[ -]',a)
        for i in range(len(b)):
            if b[i] in abbs:
                b[i] = abbs[b[i]]
        return '_'.join(b)

    class out():
        num = 4
        name = ''
        adm1 = ''
        adm2 = ''
        country = ''

    adm1 = {}
    adm2 = {}
    cou = {}
    o = {}
    addr = re.split(',[, ]*', address.strip(', '))
    if not addr:
        return []
    pri = [False for a in range(1,len(addr))]
    pri = [True] + pri
#        c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geo.geonameid,featureclass,featurecode FROM alternateNamesV2,geo WHERE (alternatename=? AND alternateNamesV2.geonameid=geo.geonameid) OR name=? ', [addr[0], addr[0]])
    tadd = fixadd(addr[0])
    c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geonameid,featureclass,featurecode FROM geo WHERE name LIKE ?', [tadd])
    ret = c.fetchall()
    c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geonameid,featureclass,featurecode FROM geo WHERE asciiname LIKE ?', [tadd])
    ret += c.fetchall()
    c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geo.geonameid,featureclass,featurecode FROM alternateNamesV2,geo WHERE (alternatename LIKE ? AND alternateNamesV2.geonameid=geo.geonameid AND isolanguage <> "iata")', [tadd])
    ret += c.fetchall()
#        print(len(ret), ret)
    geos=[]
    for item in range(len(ret)-1, -1, -1):
        if ret[item][9] in geos:
            del ret[item]
        else:
            geos.append(ret[item][9])
#        print(len(ret), ret)
    for item in range(len(ret)):
        c.execute('SELECT Countryname,geonameid FROM ISO_3166_country_codes WHERE Alpha2code=?', [ret[item][3]])
        country = c.fetchall()
        if len(country) == 1:
            if country[0][1] in cou:
                if ret[item][9] not in cou[country[0][1]]:
                    cou[country[0][1]].append(ret[item][9])
            else:
                cou[country[0][1]] = [ret[item][9]]
            o[ret[item][9]] = out()
            o[ret[item][9]].name = ret[item][0]
            o[ret[item][9]].country = country[0][0]
            o[ret[item][9]].prin = list(pri)
            if ret[item][10] == 'A':
                if ret[item][11] == 'ADM1':
                    o[ret[item][9]].num = 2
                elif ret[item][11] == 'ADM2':
                    o[ret[item][9]].num = 3
                elif 'PCL' in ret[item][11]:
                    o[ret[item][9]].num = 1
            if ret[item][5]:
                adminc1 = '{}.{}'.format(ret[item][3],ret[item][5])
                c.execute('SELECT geonameid,name FROM admin1CodesASCII WHERE code=?', [adminc1])
                admin1 = c.fetchall()
                for a1 in admin1:
                    o[ret[item][9]].adm1 = a1[1]
                    if a1[0] in adm1:
                        if ret[item][9] not in adm1[a1[0]]:
                            adm1[a1[0]].append(ret[item][9])
                    else:
                        adm1[a1[0]] = [ret[item][9]]
                if ret[item][6]:
                    adminc2 = '{}.{}'.format(adminc1,ret[item][6])
                    c.execute('SELECT geonameid,name FROM admin2Codes WHERE codes=?', [adminc2])
                    admin2 = c.fetchall()
                    for a2 in admin2:
                        o[ret[item][9]].adm2 = a2[1]
                        if a2[0] in adm2:
                            if ret[item][9] not in adm2[a2[0]]:
                                adm2[a2[0]].append(ret[item][9])
                        else:
                            adm2[a2[0]] = [ret[item][9]]
                    if ret[item][7]:
                        adminc3 = '{}.{}'.format(adminc2,ret[item][7])
                    else:
                        adminc3 = ''
                else:
                    adminc2 = ''
        else:
            adminc1 = ''
    good = {}
    for a in range(1,len(addr)):
        tadd = fixadd(addr[a])
        c.execute('SELECT name,featurecode,geonameid FROM geo WHERE name LIKE ? AND featureclass="A"', [tadd])
        ret1 = c.fetchall()
        c.execute('SELECT name,featurecode,geonameid FROM geo WHERE asciiname LIKE ? AND featureclass="A"', [tadd])
        ret1 += c.fetchall()
        c.execute('SELECT name,featurecode,geo.geonameid FROM alternateNamesV2,geo WHERE alternatename LIKE ? AND alternateNamesV2.geonameid=geo.geonameid AND featureclass="A"', [tadd])
        ret1 += c.fetchall()
        geos=[]
        for item in range(len(ret1)-1, -1, -1):
            if ret1[item][2] in geos:
                del ret1[item]
            else:
                geos.append(ret1[item][2])
        for item in ret1:
            if item[1] == 'ADM1':
                if item[2] in adm1:
                    for it in adm1[item[2]]:
                        o[it].adm1 = item[0]
                        o[it].prin[a] = True
            elif item[1] == 'ADM2':
                if item[2] in adm2:
                    for it in adm2[item[2]]:
                        o[it].adm2 = item[0]
                        o[it].prin[a] = True
            elif 'PCL' in item[1]:
                if item[2] in cou:
                    for it in cou[item[2]]:
                        o[it].country = item[0]
                        o[it].prin[a] = True

    names = set()
    for item in o:
        p = True
        for i in range(len(o[item].prin)):
            p &= o[item].prin[i]
        if p:
            names.add(name_format(o[item]))
    return list(names)

