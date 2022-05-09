import re

class nmb:
    num = 0
    name = ""
    birthdate = ""
    birthplace = ""
    deathdate = ""
    deathplace = ""
# pa parses one line from an ahnentafel
def pa(line):
    def fix1(s):
        s = s.strip()
        s = puk.sub('',s)
        s = pde.sub('',s)
        s = psc.sub(' ',s)
        s = psp.sub(' ',s)
        s = s.translate(trantab)
        return s
    def fixdate(n,m,pad):
#            print (n,m,pad)
        baddate = False
        dend = m.start()
        if n == 0:
            day = ''
            mo = ''
            yr = str(int((int(m.group(4)) + int(m.group(5)))/2))
        elif n == 1:
            day = int(m.group(2))
            mo = m.group(1).lower()
            yr = m.group(3)
        elif n == 2:
            day = int(m.group(2))
            m0 = int(m.group(1))
            yr = m.group(3)
            if m0 > 12:
                day, m0 = m0, day
            if (m0 < 1) or (m0 > 12):
                baddate = True
            else:
                mo = months[m0-1]
        elif n == 3:
            m0 = int(m.group(2))
            yr = m.group(1)
            if m0 == 0:
                day = ''
                mo = ''
            else:
                day = int(m.group(3))
                if m0 > 12:
                    day, m0 = m0, day
                if (m0 < 1) or (m0 > 12):
                    baddate = True
                else:
                    mo = months[m0-1]
        elif n == 4:
            day = int(m.group(1))
            mo = m.group(2).lower()
            yr = m.group(3)
        elif n == 5:
            day = ''
            t = m.group(1).lower()
            yr = m.group(2)
            if t in mdict:
                mo = t
                dend = m.start(1)
            else:
                mo = ''
                dend = m.start(2)
        elif n == 6:
            day = ''
            mo = ''
            m0 = int(m.group(1))
            yr = m.group(2)
            if (m0 < 1) or (m0 > 12):
                baddate = True
            else:
                mo = months[m0-1]
        elif n == 7:
            day = ''
            mo = ''
            yr = m.group(1)
        else:
            print(pla,m)
            return [pla,m.group(0)]
        if baddate:
            return ['Bad date',pad]
        pla = pad[:dend]
#            print(pla,m)
        if mo in mdict:
            mo = mdict[mo]
#            print(str(day) + ' ' +  + ' ' + m.group(1))
        return [pla,str(day) + ' ' + mo + ' ' + yr]
    xx = nmb()
    a1=p.split(line)
    if len(a1) < 3:
        print(line)
        return xx         #no born: or died:
    b1=p1.split(a1[0])   # split number from name
    if len(b1) < 2:
        return xx         #no name
    name = b1[1]
    for x in range(2,len(b1)):
        name = name+'. '+b1[x]  # if name has '. ', put it back
    xx.num = int(b1[0])
    plda = [[],[]]
    for x in range(1,3):
        for y in range(len(pdate)):
            mat=pdate[y].search(str(a1[x]))
            if mat:
                tm = fixdate(y,mat,str(a1[x]))
#                    print (x,tm)
                plda[x-1] = tm
                a1[x] = plda[x-1][0] + ', ' + plda[x-1][1]
                break
        if not mat:
            plda[x-1] = [a1[x],'']
    xx.name = fix1(name)
#        print(plda)
    try:
        xx.birthplace = fix1(str(plda[0][0]))
    except IndexError:
        pass
    try:
        xx.birthdate = fix1(str(plda[0][1]))
    except IndexError:
        pass
    try:
        xx.deathplace = fix1(str(plda[1][0]))
    except IndexError:
        pass
    try:
        xx.deathdate = fix1(str(plda[1][1]))
    except IndexError:
        pass
    return xx
months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
mdict = {'january'  : 'Jan',
            'february' : 'Feb',
            'march'    : 'Mar',
            'april'    : 'Apr',
            'may'      : 'May',
            'june'     : 'Jun',
            'july'     : 'Jul',
            'august'   : 'Aug',
            'september': 'Sep',
            'october'  : 'Oct',
            'november' : 'Nov',
            'december' : 'Dec',
            'jan' : 'Jan',
            'feb' : 'Feb',
            'mar' : 'Mar',
            'apr' : 'Apr',
            'may' : 'May',
            'jun' : 'Jun',
            'jul' : 'Jul',
            'aug' : 'Aug',
            'sep' : 'Sep',
            'sept' : 'Sep',
            'oct' : 'Oct',
            'nov' : 'Nov',
            'dec' : 'Dec',
            'janvier'  : 'Jan',
            'février'  : 'Feb',
            'mars'     : 'Mar',
            'avril'    : 'Apr',
            'mai'      : 'May',
            'juin'     : 'Jun',
            'juillet'  : 'Jul',
            'août'     : 'Aug',
            'septembre': 'Sep',
            'octobre'  : 'Oct',
            'novembre' : 'Nov',
            'décembre' : 'Dec',
            'aft'      : 'Aft.',
            'after'    : 'Aft.',
            'bef'      : 'Bef.',
            'before'   : 'Bef.',
            'abt'      : 'Abt.',
            'about'    : 'Abt.',
            'circa'    : 'Abt.'}
trantab  = ''.maketrans('‘’“”', '\'\'""')
puk = re.compile(r'\bunknown\b',re.I)
pde = re.compile(r'\bdeceased\b',re.I)
psc = re.compile(r' *\*+ *')
psp = re.compile(r'  +')
p = re.compile(r' born: ?| ?died: ?')
p1 = re.compile(r'\. ')
# pdate is a list of date formats to be converted to DD Mon YYYY
#  0 - Between date, date
#  1 - Month Day[,] Year
#  2 - MM[-/]DD[-/]YYYY or DD[-/]MM[-/]YYYY if month os out of range
#  3 - YYYY[-/]MM[-/]DD
#  4 - DD[ -/]Month[ -/]YYYY
pdate = \
[re.compile(r'((Betw?\.?)|(Between)).*([0-9]{4}).*([0-9]{4})'),
re.compile(r'([^\W\d_]{3,})[,. ]+([0-9]{1,2})[, ]+([0-9]{4})'),
re.compile(r'([0-9]{1,2})[-/. ]([0-9]{1,2})[-/. ]([0-9]{4})'),
re.compile(r'([0-9]{4})[-/]([0-9]{1,2})[-/]([0-9]{1,2})'),
re.compile(r'([0-9]{1,2})[ -/]?([^\W\d_]{3,})[.,]?[ -/]([0-9]{4})'),
re.compile(r'([^\W\d_]{3,})\.? ([0-9]{4})'),
re.compile(r'([0-9]{1,2})[ -/]([0-9]{4})'),
re.compile(r'([0-9]{4})[, ]*$')]
