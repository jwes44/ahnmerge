import tkinter as tk
from tkinter import ttk, Menu
import sqlite3
import re
from operator import itemgetter, attrgetter

#source = sqlite3.connect('e:/geonames.db')
#conn = sqlite3.connect(':memory:')
#source.backup(conn)
conn = sqlite3.connect('e:/geonames.db')
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
'Wyo.' : 'Wyoming',
'AL' : 'Alabama',
'AK' : 'Alaska',
'AZ' : 'Arizona',
'AR' : 'Arkansas',
'AS' : 'American Samoa',
'CA' : 'California',
'CO' : 'Colorado',
'CT' : 'Connecticut',
'DE' : 'Delaware',
'DC' : 'District of Col',
'FL' : 'Florida',
'GA' : 'Georgia',
'GU' : 'Guam',
'HI' : 'Hawaii',
'ID' : 'Idaho',
'IL' : 'Illinois',
'IN' : 'Indiana',
'IA' : 'Iowa',
'KS' : 'Kansas',
'KY' : 'Kentucky',
'LA' : 'Louisiana',
'ME' : 'Maine',
'MD' : 'Maryland',
'MA' : 'Massachusetts',
'MI' : 'Michigan',
'MN' : 'Minnesota',
'MS' : 'Mississippi',
'MO' : 'Missouri',
'MT' : 'Montana',
'NE' : 'Nebraska',
'NV' : 'Nevada',
'NH' : 'New Hampshire',
'NJ' : 'New Jersey',
'NM' : 'New Mexico',
'NY' : 'New York',
'NC' : 'North Carolina',
'ND' : 'North Dakota',
'OH' : 'Ohio',
'OK' : 'Oklahoma',
'OR' : 'Oregon',
'PA' : 'Pennsylvania',
'PR' : 'Puerto Rico',
'RI' : 'Rhode Island',
'SC' : 'South Carolina',
'SD' : 'South Dakota',
'TN' : 'Tennessee',
'TX' : 'Texas',
'TT' : 'Trust Territ',
'UT' : 'Utah',
'VT' : 'Vermont',
'VA' : 'Virginia',
'VI' : 'Virgin Islands',
'WA' : 'Washington',
'WV' : 'West Virginia',
'WI' : 'Wisconsin',
'WY' : 'Wyoming'
}

states = {
'Alabama',
'Alaska',
'Arizona',
'Arkansas',
'American Samoa',
'California',
'Colorado',
'Connecticut',
'Delaware',
'District of Col',
'Florida',
'Georgia',
'Guam',
'Hawaii',
'Idaho',
'Illinois',
'Indiana',
'Iowa',
'Kansas',
'Kentucky',
'Louisiana',
'Maine',
'Maryland',
'Massachusetts',
'Michigan',
'Minnesota',
'Mississippi',
'Missouri',
'Montana',
'Nebraska',
'Nevada',
'New Hampshire',
'New Jersey',
'New Mexico',
'New York',
'North Carolina',
'North Dakota',
'Ohio',
'Oklahoma',
'Oregon',
'Pennsylvania',
'Puerto Rico',
'Rhode Island',
'South Carolina',
'South Dakota',
'Tennessee',
'Texas',
'Utah',
'Vermont',
'Virginia',
'Virgin Islands',
'Washington',
'West Virginia',
'Wisconsin',
'Wyoming'
}

cns = {
'Federal Republic of Germany' : 'Germany',
'United Kingdom' : 'UK',    
'United Kingdom of Great Britain and Northern Ireland' : 'UK', 
'United States' : 'USA'
}

bad_words = {
'baptized',
'circa',
'likely',
'possibly',
'prob',
'probably',
'township',
'twp'
}

fixed_names = {}

def geoclear():
    fixed_names.clear()

def fetch_SQL(c, tadd):
    c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geonameid,featureclass,featurecode,population FROM geonames WHERE name LIKE ?', [tadd])
    ret = c.fetchall()
    c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geonameid,featureclass,featurecode,population FROM geonames WHERE asciiname LIKE ?', [tadd])
    ret += c.fetchall()
    c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geonames.geonameid,featureclass,featurecode,population FROM alternateNamesV2,geonames WHERE (alternatename LIKE ? AND alternateNamesV2.geonameid=geonames.geonameid AND (isolanguage IS NULL OR isolanguage <> "iata"))', [tadd])
    ret += c.fetchall()
    c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geonames.geonameid,featureclass,featurecode,population FROM alternateNamesV2,geonames WHERE (alternatename LIKE ? AND alternateNamesV2.geonameid=geonames.geonameid AND (isolanguage IS NULL OR isolanguage <> "iata"))', [tadd + ' Township'])
    ret += c.fetchall()
    return ret

class RightClicker:
    def __init__(self, event):
        right_click_menu = Menu(None, tearoff=0, takefocus=0)

        for txt in ['Cut', 'Copy', 'Paste', 'SelectAll']:
            right_click_menu.add_command(
                label=txt, command=lambda event=event, text=txt:
                self.right_click_command(event, text))

        right_click_menu.tk_popup(event.x_root + 40, event.y_root + 10, entry='0')

    def right_click_command(self, event, cmd):
        event.widget.event_generate(f'<<{cmd}>>')

def valname1(address,root):
    def name_format(t):
        if t.country in cns:
            t.country = cns[t.country]
        t.adm2 = t.adm2.replace(' County','') 
        n = t.name.replace(' County','')
        n = n.replace(' Township','')
        n = n.replace('Township of ','')
        if t.num == 1 and n in cns:
            n = cns[n]
        if t.num == 4:
            n = n + (', ' + t.adm2 if t.adm2 else '') + (', ' + t.adm1 if t.adm1 else '') + (', ' + t.country if t.country else '')
        elif t.num == 3:
            n = n + (', ' + t.adm1 if t.adm1 else '') + (', ' + t.country if t.country else '')
        elif t.num == 2:
            n = n + (', ' + t.country) if t.country else ''
        return n
    def fixadd(a):
        a = a.replace('...','%')
        a = a.replace('…','%')
        if a == '%':
            return ''
        b = re.split('[ -]',a)
        for i in range(len(b)):
            if b[i] in abbs:
                b[i] = abbs[b[i]]
        return '_'.join(b)

    class geofind():
        def __init__(self):
            self.topw = tk.Toplevel()
            self.find = ttk.Combobox(self.topw,width=75)
            ttk.Button(self.topw, text="OK", command=self.geocallback).grid(row=0, column=0)
            ttk.Button(self.topw, text="Cancel", command=self.geocallback1).grid(row=0, column=1)
            self.find.grid(row=0, column=2)
            self.find.bind('<Button-3>', RightClicker)

        def geocallback(self): 
            self.ret = self.find.get()
            self.topw.destroy()

        def geocallback1(self): 
            self.topw.destroy()
            self.ret = ''

        def go(self,title,nm,address):
            self.find['values'] = nm
            self.find.set(address)
            self.topw.title(title)
            self.topw.wm_deiconify()
            self.topw.grab_set()
            self.topw.wait_window(self.topw)
            return self.ret


    class out():
        num = 4
        name = ''
        adm1 = ''
        adm2 = ''
        country = ''
        prin = 1

    adm1 = {}
    adm2 = {}
    cou = {}
    o = {}
    addr = []
    address = address.strip(', ')
    taddr = re.split(',[, ]*', address)
    for i in range(len(taddr)):
        taddr[i] = re.sub('^St([ -])',r'Saint\1',taddr[i])
        taddr[i] = re.sub(' Co(unty$|$)','',taddr[i])
        if i == len(taddr) - 1:
            taddr[i] = re.sub('United S.*','USA',taddr[i])
        xaddr = taddr[i].split(' ')
        for j in range(len(xaddr)):
            if xaddr[j].lower() in bad_words:
                del xaddr[j]
        taddr[i] = ' '.join(xaddr)
    address = ', '.join(taddr)
    if len(taddr) == 1:
        if address in states:
            return address + ', USA'
        elif address in abbs:
            return abbs[address] + ', USA'
        else:
            xaddr = taddr[0].split(' ')
            if len(xaddr) > 1 and (xaddr[1] == 'USA' or xaddr[1] == 'United'):
                if xaddr[0] in states:
                    return xaddr[0] + ', USA'
                elif xaddr[0] in abbs:
                    return abbs[xaddr[0]] + ', USA'
    for a in range(len(taddr)):
        n = fixadd(taddr[a])
        if n:
            addr.append(n)
    if not addr:
        return ''
    if address in fixed_names:
        return fixed_names[address]
    pri = [False for a in range(1,len(addr))]
    pri = [True] + pri
#        c.execute('SELECT name,latitude,longitude,countrycode,cc2,admin1code,admin2code,admin3code,admin4code,geonames.geonameid,featureclass,featurecode,population FROM alternateNamesV2,geonames WHERE (alternatename=? AND alternateNamesV2.geonameid=geonames.geonameid) OR name=? ', [addr[0], addr[0]])
    tadd = fixadd(addr[0])
    ret = fetch_SQL(c, tadd)
#        print(len(ret), ret)
    if not ret:
        ret = fetch_SQL(c, '%'+tadd+'%')
    geos=[]
    for item in range(len(ret)-1, -1, -1):
        if ret[item][9] in geos:
            del ret[item]
        else:
            geos.append(ret[item][9])
#        print(len(ret), ret)
    top = [0,0,0,0,0]
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
            if ret[item][10] == 'A':
                if ret[item][11] == 'ADM1':
                    o[ret[item][9]].num = 2
                elif ret[item][11] == 'ADM2':
                    o[ret[item][9]].num = 3
                elif 'PCL' in ret[item][11]:
                    o[ret[item][9]].num = 1
            top[o[ret[item][9]].num ] = 1
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
        c.execute('SELECT name,featurecode,geonameid FROM geonames WHERE name LIKE ? AND featureclass="A"', [tadd])
        ret1 = c.fetchall()
        c.execute('SELECT name,featurecode,geonameid FROM geonames WHERE asciiname LIKE ? AND featureclass="A"', [tadd])
        ret1 += c.fetchall()
        c.execute('SELECT name,featurecode,geonames.geonameid FROM alternateNamesV2,geonames WHERE alternatename LIKE ? AND alternateNamesV2.geonameid=geonames.geonameid AND featureclass="A"', [tadd])
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
                        o[it].prin += 2 ** a
            elif item[1] == 'ADM2':
                if item[2] in adm2:
                    for it in adm2[item[2]]:
                        o[it].adm2 = item[0]
                        o[it].prin += 2 ** a
            elif 'PCL' in item[1]:
                if item[2] in cou:
                    for it in cou[item[2]]:
                        o[it].country = item[0]
                        o[it].prin += 2 ** a

    names = set()
    tnames = set()
    n2 = False
    for j in range(len(top)):
        if top[j]:
            madmn = j
            break
    for item in o:
#    for item in sorted(o, key=attrgetter('num')):
        p = True
        if len(addr) == 1:
            if o[item].num == madmn:
                names.add(name_format(o[item]))
        elif len(addr) == 2 and o[item].prin == 3:
#            print('==>', address, '|', name_format(o[item]))
            if o[item].num == madmn:
                names.add(name_format(o[item]))
                n2 = True
            else:
                tnames.add(name_format(o[item]))
        elif o[item].prin == 2 ** len(addr) - 1:
            names.add(name_format(o[item]))
    if not n2:
        names = names | tnames
    if len(names) == 1:
        [rv] = names
        fixed_names[address] = rv
        return rv
    if address in names:
        fixed_names[address] = address
        return address
    if len(addr) > 2:
        address1 = re.sub(' ?\.\.\.', '', address)
        for i in names:
            if re.match(address1, i, flags=re.IGNORECASE):
                fixed_names[address] = i
                fixed_names[address1] = i
                return i

    if names:
        gf = geofind()
        rv = gf.go("Multiple", list(names),address)
        if rv:
            fixed_names[address] = rv
        return rv
    else:
        for item in o:
            p = True
            if o[item].prin == 2 ** len(addr) - 3:
                names.add(name_format(o[item]))
        if names:
            gf = geofind()
            rv = gf.go("No exact match", list(names),address)
            if rv:
                fixed_names[address] = rv
            return rv

    return ''

class notfind():
    def __init__(self):
        self.topw = tk.Toplevel(height=80,bg = 'light green')
        self.find = ttk.Entry(self.topw,width=75)
        ttk.Button(self.topw, text="OK", command=self.notcallback).grid(row=0, column=0)
        ttk.Button(self.topw, text="Cancel", command=self.notcallback1).grid(row=0, column=1)
        self.find.grid(row=0, column=2)
        self.find.bind('<Button-3>', RightClicker)

    def notcallback(self): 
        self.ret = self.find.get()
        self.topw.destroy()

    def notcallback1(self): 
        self.topw.destroy()
        self.ret = ''

    def go(self,title,address):
        self.find.insert(0,address)
        self.topw.title(title)
        self.topw.wm_deiconify()
        self.topw.grab_set()
        self.topw.wait_window(self.topw)
        return self.ret

def valname(address,root):
    rv = ''
    while True:
        a = valname1(address,root)
        if a:
            if rv:
                fixed_names[rv] = a
            return a
        n = notfind()
        rv = n.go("No Match", address)
        if rv:
            address = rv
        else:
            return address
