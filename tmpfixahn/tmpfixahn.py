
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class nmb:
    num = 0
    name = ""
    birthdate = ""
    birthplace = ""
    deathdate = ""
    deathplace = ""

def pa(line):
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
#        from string import maketrans
    trantab  = ''.maketrans('‘’“”', '\'\'""')
    puk = re.compile(r'\bunknown\b',re.I)
    pde = re.compile(r'\bdeceased\b',re.I)
    psc = re.compile(r' *\*+ *')
    psp = re.compile(r'  +')
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

def parseahn(ahn, lines, off=1):
    def nti(l1,s):
        pnb = re.compile(r'[^ ,.]')
        if pnb.search(s):
            for z1 in range(len(l1)):
                if l1[z1] == s:
                    return
            l1.append(s)
    for line in lines:
#            print(line)
        ao=pa(line)
        num = ao.num
        if num == 0:
            continue
        if off > 1:
            x=1
            while x*2 <= num:
                x = x*2
            num = off * x + num % x
#                print(num,b1[0],a1[0])
        if num not in ahn:
            ahn[num] = [[],[],[],[],[]]
        nti(ahn[num][0],ao.name)
#            print(plda)
        try:
            nti(ahn[num][1],ao.birthplace)
        except IndexError:
            pass
        try:
            nti(ahn[num][2],ao.birthdate)
        except IndexError:
            pass
        try:
            nti(ahn[num][3],ao.deathplace)
        except IndexError:
            pass
        try:
            nti(ahn[num][4],ao.deathdate)
        except IndexError:
            pass


class AhnMerge():
    ahn = {1 : [['Private'], [], [], [], []],
2 : [['Private'], [], [], [], []],
3 : [['Private'], [], [], [], []],
4 : [['Private'], [], [], [], []],
5 : [['Elaine Elva Gilchrist'], ['Ohio, United States, '], [' 1929'], ['United States, '], ['22 Apr 1992']],
6 : [['Russell Ray Shope'], [', Poweshiek, Iowa, '], ['3 May 1926'], ['Coolidge,, AZ, '], ['2 Jul 1981']],
7 : [['Anna Lou DuPre'], ['Iowa, United States, '], ['29 May 1925'], ['United States, '], ['19 Feb 2003']],
8 : [['Joseph F Brown', 'Joseph F. Brown'], ['New Castle, Pennsylvania, ', 'United States, '], ['5 Nov 1874', ' 1874'], ['New Castle, Lawrence...ania,..., '], ['23 Jan 1948']],
9 : [['Laura A. Stewart'], ['United States, '], [' 1886'], [], []],
10 : [['Leslie Gilchrist'], ['Pennsylvania, United States, ', 'United States, '], [' 1905'], ['Trumbull County, Ohio, USA, '], ['21 Jun 1988']],
11 : [['Beulah F. Eshleman'], ['Ohio, United States, '], [' 1906'], [], []],
12 : [['Ray Russell Shope'], ['United States, '], ['6 Jun 1900'], ['United States, '], ['21 Jun 1961']],
13 : [['Lovina Marie Fogel'], ['United States, '], ['31 Mar 1904'], ['United States, '], ['9 Aug 1982']],
14 : [['Edison Lee DuPre', 'Edison Lee Dupre'], ['Vining Tama, Iowa, ', 'Iowa, '], ['25 Nov 1899'], ['United States, '], ['8 Jun 1973']],
15 : [['Lillian Anna Kunc', 'Lillie Kunch'], ['Toledo, Iowa, ', 'Iowa, '], ['9 Nov 1900'], ['AZ, '], ['23 Jun 1968']],
20 : [['George Melvin Gilchrist', 'Gilchrist'], ['Clarion, Pennsylvania, USA, '], ['25 Nov 1877'], [], []],
24 : [['Jacob Farney Shope', 'Jacob Forney Shope'], ['Girard, Clearfield, ...nia, USA, ', 'United States, '], ['27 Jun 1870'], ['Tama, Iowa, USA, ', 'United States, '], ['4 Mar 1942', '2 Feb 1942']],
25 : [['Alma Lorena Babb'], ['Highland, Tama, IA, ', 'Highland twp,Tama co, Iowa, '], ['17 Jan 1876'], ['Sheridan twp Poweshi...co, Iowa, ', 'Poweshiek, IA, '], ['15 Nov 1928']],
26 : [['George Edward Fogel'], ['Sheridan, Poweshiek, Iowa, ', 'United States, '], ['17 Apr 1878'], ['Iowa, USA, ', 'United States, '], ['9 Jun 1956']],
27 : [['Susie Lovina Clark', 'Susie Louisa Clark'], ['Haven, Tama Co, IA, US, ', ', Tama, Iowa, USA, '], [' Nov 1881', '26 Nov 1882'], ['IA, US, '], ['30 Apr 1959']],
28 : [['Celestian Charles DuPre', 'Celestin Charles Dupre'], [', Iowa, USA, ', 'Iowa, USA, '], ['12 Sep 1863'], ['Toledo, Iowa, USA, '], ['18 Nov 1938', ' 1938']],
29 : [['Anna Maria Liskovec', 'Anna Mary Liskovec'], ['Iowa, United States, ', 'Czecho-Slovakia, '], [' Jul 1876', ' 1876'], ['Iowa, United States, ', 'Tama County, Iowa, USA, '], [' 1929', ' 1923']],
30 : [['Martin Kunc', 'Martin Kunch'], ['Bohemia, ', 'Czechoslovakia, '], ['6 Dec 1861', ' 1861'], ['Iowa, '], ['10 Dec 1937', ' 1937']],
31 : [['Anna Maria Novotny', 'Anna Novotny'], ['Bohemia, ', 'Czechoslovakia, '], [' Apr 1861'], ['Tama County, Iowa, '], ['18 Aug 1942']],
16 : [['Thomas Braun'], ['Germany, '], ['22 Sep 1845'], ['Pennsylvania, USA, '], ['29 Sep 1895']],
17 : [['Stephania Rohrer'], ['Germany, '], ['4 Dec 1850'], ['Pennsylvania, USA, '], ['18 Sep 1933']],
32 : [['Andreas Braun'], [], [], [], []],
33 : [['Maria Futterer'], ['Freiburg, Baden, '], ['3 Mar 1815'], ['Baden, Germany, '], ['10 Oct 1868']],
34 : [['Joseph W Rohrer'], ['Freiburg, Baden, '], ['10 Jan 1823'], [], []],
35 : [['Maria Steiert'], ['Freiburg, Baden, '], ['23 Feb 1827'], [], ['3 Sep 1909']],
64 : [['Thomas Braun'], [], [' 1778'], [], [' 1827']],
65 : [['Ursula Kürner'], [], [], [], []],
68 : [['Johannes Rohrer'], ['Deutschland, '], ['22 Aug 1796'], ['Deutschland, '], ['14 Nov 1828']],
69 : [['Francisca Fehrenbach'], ['Freiburg, Baden, '], ['13 Mar 1789'], ['Freiburg, Baden, '], ['22 Apr 1860']],
70 : [['Andreas Steiert'], ['Freiburg, Baden, '], [' Abt. 1777'], [], []],
71 : [['Maria Francisca Scherer'], ['Freiburg, Baden, '], ['2 Mar 1788'], ['Freiburg, Baden, '], ['22 Dec 1864']],
128 : [['Jacobus Braun'], ['Germany, '], ['13 Jul 1729'], ['Germany, '], ['24 Jun 1793']],
129 : [['Johanna Blattmann'], ['Germany, '], ['27 Aug 1737'], ['Germany, '], ['6 Jan 1789']],
130 : [['Joannes Kuerner'], ['St Peter, Baden, Germany, '], [' 1749'], [], [' 1842']],
131 : [['Maria Zimmermann'], ['St Peter, , Germany, '], [' 1753'], [], []],
136 : [['Johann Evangelist Rohrer'], ['Deutschland, '], ['24 Dec 1765'], [], []],
137 : [['Ursula Kirner'], ['Deutschland, '], ['27 Jul 1759'], ['Deutschland, '], ['16 Dec 1828']],
138 : [['Georgius Georg FEHRENBACH'], ['Deutschland, '], ['21 Aug 1754'], ['Deutschland, '], ['14 May 1805']],
139 : [['Maria Hettich'], ['Freiburg, Baden, '], ['16 Apr 1754'], ['Freiburg, Baden, '], ['12 May 1829']],
142 : [['Jacobus Scherer'], ['Deutschland, '], ['15 Jul 1753'], ['Deutschland, '], ['31 Oct 1829']],
143 : [['Catharina Rohrer'], ['Freiburg, Baden, '], ['2 Oct 1761'], ['Freiburg, Baden, '], ['13 Apr 1841']],
21 : [['Nancy Etta Pugh'], ['Pennsylvania, '], ['1 Nov 1880'], ['Wall, Pennsylvania, USA, '], ['25 Apr 1910']],
40 : [['John Gilchrist'], ['Pennsylvania, USA, '], ['4 Apr 1842'], ['Pennsylvania, USA, '], ['7 Aug 1934']],
41 : [['Polly Gilchrist'], ['Pennsylvania, '], [' Abt. 1844'], ['Pennsylvania, USA, '], ['18 Feb 1922']],
43 : [['?Alice Agnew?'], ['Scotland, '], [' 1839'], [], []],
80 : [['Thomas Gilchrist'], ['Ohio, USA, '], ['18 Dec 1812'], ['Ohio, USA, '], ['29 Jun 1852']],
81 : [['Lucinda Gilbert'], ['Westmoreland County Pa, '], [' 1814'], ['USA, '], ['18 Nov 1895']],
83 : [['Marriah Davis'], [], [' 1824'], [], []],
160 : [['Willilam Gilchrist'], ['Pennsylvania, USA, '], ['13 Aug 1782'], ['Ohio, USA, '], ['19 Feb 1835']],
161 : [['Jane Orr'], ['Cumberland Co., PA, '], [' 1785'], ['Richland Co., Ohio, '], [' 1833']],
162 : [['John GILBERT'], ['New York, USA, '], [' 1787'], ['USA, '], ['28 Mar 1866']],
22 : [['Henry Eshleman'], ['Wayne, Ohio, '], ['5 Apr 1876'], [], ['22 Jul 1918']],
44 : [['Jacob M. Eshleman'], ['Ohio, '], [' 1845'], ['Wayne County, Ohio, '], ['29 Oct 1935']],
45 : [['Nancy Kornhaus Eshleman'], ['Ohio, USA, '], ['29 Apr 1849'], [], ['20 Nov 1920']],
88 : [['John S Eshelman'], ['Pennsylvania, USA, '], ['17 Nov 1809'], ['Wayne County, Ohio, '], ['1 May 1866']],
89 : [['Mary Ann Hart Eshleman'], ['Pennsylvania, '], [' 1819'], ['Pennsylvania, '], ['26 Oct 1882']],
90 : [['Henry Kornhaus'], ['United States, '], ['15 Apr 1816'], ['United States, '], ['30 Nov 1884']],
91 : [['SUSAN BRENNEMAN'], ['Pennsylvania, '], ['1 Apr 1820'], ['Ohio, USA, '], ['31 Mar 1899']],
176 : [['Jacob Eshelman'], ['Pennsylvania, '], ['8 Feb 1778'], ['USA, '], ['30 Dec 1815']],
177 : [['Elizabeth Stauffer'], ['Pennsylvania, USA, '], ['4 Mar 1784'], ['Ohio, USA, '], ['18 Mar 1870']],
180 : [['John Kornhaus'], ['United States, '], [' 1774'], ['United States, '], [' 1818']],
181 : [['anna Culbertson'], [], [' 1780'], [], [' 1821']],
183 : [['Nancy Anna Eymann'], ['United States, '], ['18 Jun 1791'], ['United States, '], ['15 Feb 1871']],
352 : [['Jacob K Eshleman'], ['United States, '], [' 1738'], ['United States, '], ['8 Jan 1794']],
353 : [['Elizabeth Kauffman '], [], [' 1753'], ['United States, '], ['28 Mar 1805']],
360 : [['JOHANNES KORNHAAS'], ['Switzerland, '], [' Abt. 1735'], ['Pennsylvania, USA, '], [' Jun 1783']],
361 : [['Mary Culbertson'], ['Switzerland, '], [' Abt. 1740'], ['USA, '], [' Bef. 1821']],
23 : [['Elva Alice Bair'], ['Wayne, Ohio, USA, '], ['31 Jan 1880'], ['Akron, Summit, Ohio, USA, '], ['3 Mar 1948']],
46 : [['David Bair'], ['Ohio, '], [' Mar 1856'], [], ['2 Oct 1918']],
47 : [['Francis Forrer'], ['East Union, Wayne, Ohio, USA, '], ['19 Sep 1859'], ['Rittman, Ohio, USA, '], ['7 Feb 1945']],
92 : [['Daniel Bair'], ['USA, '], ['6 Sep 1818'], ['Ohio, USA, '], ['22 May 1890']],
93 : [['Harriet Mowrer'], ['United States of, '], ['19 Aug 1820'], ['United States, '], ['13 Dec 1892']],
94 : [['John P Forrer'], ['Pennsylvania, USA, '], ['10 Sep 1815'], ['United States, '], ['5 Jul 1889']],
95 : [['Mary Ann Meck'], ['PA, '], ['10 Nov 1823'], ['United States, '], ['24 Feb 1901']],
184 : [['Joel Bear'], ['USA, '], ['18 Dec 1784'], ['United States, '], ['3 Jan 1829']],
185 : [['Anna Maria Wolf'], ['USA, '], ['30 Oct 1788'], ['USA, '], ['22 Jan 1839']],
186 : [['Henry Mowrer'], ['Pennsylvania, USA, '], [' 1784'], ['Ohio, USA, '], ['27 Nov 1865']],
187 : [['Catharine Mowrer'], ['Chester C, PA, '], [' Abt. 1789'], ['Wayne C Ohio, '], ['28 Jun 1866']],
188 : [['Martin F. Forrer'], ['United States, '], ['8 Nov 1765'], ['United States, '], ['26 Jun 1854']],
190 : [['John "George" Elmer Meck'], [], ['29 Oct 1782'], [], ['7 May 1870']],
191 : [['Martha Nudding'], ['Wuerttemberg, '], ['21 Feb 1797'], ['USA, '], ['11 Jun 1869']],
368 : [['George Eby Bear'], ['United States, '], [' 1750'], ['Pennsylvania, USA, '], [' 1833']],
369 : [['Mary Eby'], ['United States, '], ['20 Dec 1752'], ['United States, '], ['28 Mar 1824']],
370 : [['Jacob W. Wolf'], ['Maryland, '], ['6 Mar 1767'], ['Maryland, USA, '], ['3 Nov 1832']],
371 : [['Anna Mary Christina " Mentzer'], ['United States, '], ['23 Mar 1767'], ['Maryland, '], ['19 Feb 1833']],
372 : [['Daniel Maurer'], ['Pennsylvania, USA, '], [' 1755'], ['Pennsylvania, USA, '], [' 1807']],
373 : [['Mary Kissel'], ['Pennsylvania, USA, '], [' 1755'], ['Pennsylvania, USA, '], [' 1794']],
374 : [['Peter Dampman'], ['Pennsylvania, USA, '], ['12 Aug 1754'], ['United States, '], ['29 Jul 1804']],
375 : [['Maria Catherina Schenkel'], ['Germany, '], ['30 Oct 1746'], ['United States, '], ['2 Oct 1823']],
377 : [['Elizabeth Mylin'], ['Pennsylvania, USA, '], ['6 Apr 1741'], ['Pennsylvania, USA, '], ['6 Apr 1811']],
380 : [['Phillipp Peter Meck'], ['USA, '], ['27 Feb 1757'], ['USA, '], ['21 Nov 1844']],
381 : [['Catherine Ament'], ['USA, '], ['3 Oct 1752'], ['USA, '], [' Sep 1821']],
382 : [['Johann Melchior Nuding'], ['Württemberg, '], ['15 Oct 1768'], [], []],
383 : [['Anna Maria Siglen'], [' 9 Sept'], [], [], []],
48 : [['Andrew Gregg Shope'], ['Girard, Clearfield Co. PA, '], ['16 May 1842'], ['Pennsylvania, USA, '], ['25 May 1920']],
96 : [['Jacob Shope Jr.'], ['Pennsylvania, '], [' 1800'], ['Pennsylvania, USA, '], ['16 Jan 1879']],
97 : [['Mary Forney'], ['Pennsylvania, '], ['18 May 1805'], ['Pennsylvania, USA, '], ['27 Feb 1887']],
192 : [['Jacob Shope Sr'], ['Pennsylvania, USA, '], [' 1764'], [], ['26 Apr 1851']],
193 : [['Elizabeth Ann Hart'], [], ['20 Sep 1777'], [], ['24 Feb 1851']],
194 : [['Joseph Forney'], [], [], [], []],
195 : [['Caterina Rauchen'], [], [], [], []],
384 : [['Bernhard Shope'], ['Arrived Philadelphia, '], [' 1731'], ['USA, '], [' Aug 1813']],
385 : [['Anna Barbara Meder (Maeder)'], ['Germany, '], ['14 Jun 1735'], ['Pennsylvania, USA, '], ['8 Feb 1780']],
49 : [['Louise Minerva Smith Shope'], ['Clearfield, Pennsylv...nia, USA, '], ['26 Nov 1848'], ['Lawrence, Clearfield...nia, ..., '], ['17 Nov 1926']],
98 : [['George B Smith'], ['Pennsylvania, USA, '], ['25 Apr 1798'], ['Pennsylvania, USA, '], ['27 Aug 1879']],
99 : [['Minerva Graham'], ['United States, '], ['1 Mar 1810'], ['United States, '], ['28 Jul 1897']],
196 : [['Stephen Gerard Smith'], ['United States, '], [' 1750'], ['United States, '], ['30 Jun 1802']],
197 : [['Mary Elizabeth Straub'], ['Freeburg, Snyder Co PA, '], [' 1755'], ['Potter, Pennsylvania, USA, '], [' 1807']],
198 : [['Robert Graham'], ['United States of America, '], [' 1766'], ['United States of America, '], [' 1829']],
199 : [['Elizabeth "Betsy" Wall Jeffrey'], ['Pennsylvania, USA, '], [' 1770'], ['United States, '], ['9 Apr 1828']],
392 : [['John Smith'], ['Connecticut, USA, '], ['3 Jan 1706'], ['United States, '], ['8 Jun 1783']],
393 : [['Mary Pettit Beard'], ['Connecticut, '], ['9 Apr 1706'], ['Connecticut, USA, '], ['25 May 1776']],
394 : [['Johan Peter Straub II'], ['Germany, '], ['4 Feb 1728'], ['United State, '], ['5 Sep 1804']],
395 : [['Catharina Elisabetha Armin'], ['Germany, '], ['18 Mar 1732'], ['United States, '], ['15 Nov 1813']],
396 : [['Thomas E. Graham'], ['Augusta Co., VA or PA, '], [' 1735'], ['United States, '], ['17 Jun 1798']],
397 : [['Mary Owens'], ['Dublin, Ireland, '], ['25 May 1726'], ['Pennsylvania USA, '], [' 1794']],
398 : [['Richard Jeffrey'], ['United States, '], ['19 Oct 1726'], ['United States, '], ['4 Oct 1794']],
399 : [['Rebecca Wall Jeffrey'], ['New Jersey, USA, '], [' 1739'], ['Shrewsbury NJ, '], ['21 Jan 1793']],
784 : [['John Smith'], ['United States, '], ['3 Sep 1673'], ['United States, '], ['17 Dec 1768']],
785 : [['Mehitabel Talmadge'], ['United States, '], ['13 Dec 1686'], ['United States, '], ['7 Aug 1750']],
786 : [['Jeremiah Beard'], ['Connecticut, '], ['16 Apr 1672'], ['USA, '], ['2 Nov 1744']],
787 : [['Martha Mercy Pettit'], ['United States of A, '], ['5 Sep 1674'], ['United State, '], ['21 Feb 1761']],
788 : [['Johan Peter Straub'], ['Germany, '], ['18 Feb 1695'], ['Pennsylvania, '], ['23 Apr 1760']],
789 : [['Anna Maria Barbara Hoffman'], ['Germany, '], ['21 Aug 1696'], ['Pennsylvania, '], ['23 Apr 1760']],
790 : [['Johann Philipp Armann'], ['Germany, '], [' 1700'], [], []],
791 : [['Barbara Armin'], ['Germany, '], ['29 juli 1724'], ['USA, '], ['23 Apr 1760']],
792 : [['Robert Graham'], ['Lancaster, Pennsylvania, '], [' 1702'], ['VA, USA, '], ['21 Sep 1763']],
793 : [['Jean Hicklin'], ['United States, '], [' 1723'], ['United States, '], [' 1805']],
794 : [['Henry Owens'], ['Ireland, '], [' 1700'], [' Ireland'], []],
795 : [['Agnes Elizabeth Hughes'], ['Ireland, '], [' 1705'], [], []],
796 : [['Francis (Jr) Jeffrey'], ['New Jersey, '], ['19 Jun 1684'], ['New Jersey, '], ['22 Apr 1787']],
797 : [['Mary Blight'], [], [' 1692'], ['United States, '], [' 1784']],
798 : [['Jarrat Wall'], ['United States of, '], ['16 Mar 1691'], ['New Jersey, USA, '], ['11 May 1771']],
799 : [['Mary Pew'], ['New Jersey, USA, '], ['31 Apr 1700'], ['New Jersey, USA, '], ['4 Aug 1776']],
50 : [['Anthony L Babb'], ['Summit, Ohio, '], ['25 Feb 1841'], ['Montour, Tama, Iowa, '], ['17 Apr 1898']],
51 : [['Milly Ann Richards'], ['Ohio, '], ['25 Dec 1841'], ['Montour, Iowa, USA, '], ['17 May 1917']],
100 : [['DAVID A BABB JR.'], ['Pennsylvania, USA, '], ['1 Dec 1812'], ['United States, '], ['24 Dec 1878']],
101 : [['Elizabeth "Betsey" (...rt ) Ba...'], ['Pennsylvania, USA, '], ['17 Jun 1816'], [], []],
102 : [['Rowland Richards'], ['Ohio, United States, '], ['3 Jun 1806'], ['United States of Am, '], ['26 Sep 1887']],
103 : [['Tacy RICHARDS...', 'Lacy Walker'], ['Loudoun, Virginia, USA, ', 'Virginia, '], ['10 May 1804', ' Abt. 1805'], ['Sandyville, Jackson,...ia, U..., '], ['24 May 1872', '24 May 1870']],
200 : [['DAVID BABB Sr.'], ['Pennsylvania, USA, '], [' 1777'], ['Springfield, Ohio, USA, '], [' 1862']],
201 : [['Susan MARKS'], ['United States, '], [' 1790'], ['Ohio, United States, '], [' 1850']],
202 : [['Anthony Bachert'], ['Pennsylvania, USA, '], [' 1785'], ['Indiana, United States, '], [' 1852']],
203 : [['Catherine Ebner'], ['Pennsylvania, '], [' 1789'], ['USA, '], [' Dec 1829']],
204 : [['Abijah Richards'], ['Virginia, '], ['23 May 1753'], ['United State, '], ['14 Feb 1824']],
205 : [['Mary'], [], [], [], []],
400 : [['Mathias Babb'], ['USA, '], ['31 May 1754'], ['Pennsylvania, USA, '], ['8 Jan 1813']],
401 : [['MARIA ROSINA BEYERLE'], ['USA, '], ['22 Oct 1759'], ['Pennsylvania, USA, '], ['6 Mar 1839']],
404 : [['NICHOLAS BACHERT'], [], [], ['Pennsylvania, USA, '], [' 1824']],
405 : [['Susannah Bock'], ['Germany, '], ['20 Oct 1751'], [], []],
406 : [['Johan Lorentz Ebner'], ['Pennsylvania, '], ['25 Feb 1762'], ['Pennsylvania, '], ['10 Nov 1842']],
408 : [['Roland Richards'], ['Great Britain, '], ['29 Oct 1728'], ['United States, '], ['21 May 1815']],
409 : [['Mary Miles'], ['USA, '], ['25 Oct 1727'], ['United States, '], ['9 Dec 1766']],
206 : [['Isaac Richards'], ['Loudon, , Virginia, USA, '], ['17 Sep 1767'], [', West Virginia, USA, '], ['16 Apr 1844']],
207 : [['Deborah Drake'], ['Virginia, United States, '], ['9 May 1773'], ['United States, '], ['1 Dec 1827']],
52 : [['George Fogel'], ['Germany, '], ['4 Sep 1847'], ['United States of Americ, '], ['27 Jan 1899']],
53 : [['Mary A Glixner'], ['Cincinnati, Ohio, USA, '], ['30 Apr 1854'], ['Malcom, Iowa, USA, '], ['22 Nov 1939']],
106 : [['John Sr. Glixner'], ['Germany, '], [' Abt. 1814'], ['Indiana, '], [' Bef. 1900']],
107 : [['Theresia'], ['Germany, '], ['10 Mar 1830'], ['Jennings, Indiana, '], ['30 Dec 1875']],
54 : [['Gerry Eldridge Clark'], ['Richmond, Wayne Co, IN, US, '], ['2 May 1856'], ['Tama, Tama Co, IA, US, '], ['10 Nov 1923']],
55 : [['Della Viola Reed'], ['Winneshiek Co, IA, US, '], ['22 Feb 1858'], ['Tama Co, IA, US, '], [' 1928']],
108 : [['William C Clark 1'], ['Clinton, OH, US, '], ['20 Jan 1826'], ['Tama Co, IA, US, '], ['10 Jul 1902']],
109 : [['Sarah L Johnson'], ['NC, US, '], ['23 Jun 1829'], ['Richland, IA, US, '], ['22 Feb 1903']],
110 : [['Josephus Reed'], ['OH, US, '], ['10 Oct 1810'], ['Tama, IA, US, '], ['29 Mar 1891']],
111 : [['Nancy Rice'], ['Union, Union Co, OH, US, '], [' 1813'], ['Tama Co, IA, US, '], [' Jul 1894']],
216 : [['John Clark'], ['PA, US, '], ['14 Jul 1799'], ['Union, IA, US, '], ['16 Mar 1875']],
217 : [['Sarah Rice Wright'], ['Caroline Co, MD, US, '], [' 1799'], ['IN, US, '], [' 1838']],
220 : [['David Reed'], ['York Co, PA, US, '], [' 1776'], ['OH, US, '], ['30 Jun 1824']],
221 : [['Margaret Kirkpatrick'], ['Lancaster Co, PA, US, '], [' 1770'], ['Union City, OH, US, '], [' 1840']],
222 : [['Squire Rice 1'], ['MA, US, '], ['8 Apr 1776'], ['OH, US, '], ['8 Jan 1853']],
223 : [['Catherine Winch'], ['Roxbury, MA, US, '], ['20 Sep 1778'], ['OH, US, '], ['16 Jun 1819']],
432 : [['William Clark'], [], [' Abt. 1769'], [], []],
433 : [['Katherine Hollaway'], [], [' Abt. 1770'], [], []],
434 : [['Nathan Wright'], ['Northwest Fork, MD, US, '], [' 1753'], [], ['31 Dec 1838']],
435 : [['Esther Harris'], ['Easton, MD, US, '], ['1 Jan 1763'], ['Milford, IN, US, '], ['31 Dec 1838']],
440 : [['Thomas Reed 1'], ['Straban Twp, PA, US, '], [' Abt. 1735'], ['Georges Twp, PA, US, '], [' 1791']],
441 : [['Elizabeth Rachel Miller'], ['PA, '], [' 1745'], [' Union City, Union Co, OH, US'], []],
442 : [['Samuel Kirkpatrick 2'], ['Lancaster Co., PA, '], [' 1763'], ['Union Co., OH, '], ['1 Aug 1824']],
443 : [["Jane 'Jean' Mitchell"], ['Lancaster Co., PA, '], [' 1758'], ['Union Co., OH, '], ['6 Oct 1824']],
444 : [['Obadiah Rice 2'], ['MA, US, '], ['19 Jan 1747'], ['VT, US, '], ['7 Jan 1826']],
445 : [['Hannah Hill'], ['MA, US, '], ['17 Apr 1749'], ['VT, US, '], ['29 May 1828']],
446 : [['Jason Winch Deacon'], ['MA, US, '], ['1 Sep 1751'], ['VT, US, '], ['2 Jul 1838']],
447 : [['Abigail Howe'], ['MA, US, '], ['2 Jun 1750'], ['VT, US, '], ['14 Aug 1824']],
56 : [['Jean Pierre Dupre'], ['France, '], ['5 Mar 1817'], ['Iowa, USA, '], ['22 Sep 1888']],
57 : [['Rose Boucher'], ['France, '], ['18 Jun 1823'], ['Iowa, USA, '], ['16 Mar 1902']],
58 : [['Jan Liskovec'], ['Bohemia, '], ['18 Mar 1833'], ['Vining, Iowa, USA, '], ['2 Jun 1928']],
59 : [['Anna Kucera Liskovec'], ['Bohemia, '], ['4 Jun 1854'], ['Tama County, Iowa, '], ['9 Aug 1903']],
60 : [['Henry Kunch'], ['Bohemia, New York, USA, '], [' 1834'], ['Tama, Iowa, United States, '], [' 1911']],
61 : [['Frances Dvorak'], ['Czechoslovakia, '], [' 1834'], [], [' 1896']],
62 : [['Vencel Novotny'], ['Tabor, Bohemia, '], ['23 Aug 1838'], ['Tabor, Bohemia, '], ['28 Oct 1838']],
63 : [['Kate Vulva'], ['Bohemia, '], [' Aug 1898'], [], []],
124 : [['Jan Novotny'], ['Czech Republic, '], ['16 May 1807'], ['Tabor, Bohemia, '], ['27 Nov 1875']],
125 : [['Annie Doudova'], ['Tabor, Bohemia, '], [' Abt. 1803'], ['Bohemia, '], ['6 Oct 1886']],
248 : [['Vaclav Novotny'], ['Tabor, Bohemia, '], [' Abt. 1783'], ['Bohemia, '], ['21 Sep 1843']],
249 : [['Katherina Smrz'], ['Tabor, Bohemia, '], [' Abt. 1780'], ['Bohemia, '], ['28 Nov 1840']],}
    def callback1(self):
        def fixname(n):
            if n:
                n = n.title()
#                n = re.sub(' i*[iv] ', ' ', n, flags=re.IGNORECASE)
                n = re.sub('\.', '', n)
                n = re.sub('__+', '', n)
            return n
        root.clipboard_clear()  # clear clipboard contents
        cls()
        line = 0
        temp = {}
        keys =sorted(self.ahn)
        for x in range (len(keys)):
            y = self.ahn[keys[x]]
            o = [keys[x]]
            for i in range(5):
                o.append(y[i][0] if y[i] else '')
            o[3] = fxdate(o[3])
            o[5] = fxdate(o[5])
            if o[2]:
              bor = f'{o[2]}, {o[3]}'
            else:
              bor = o[3]
            if o[4]:
              die = f'{o[4]}, {o[5]}'
            else:
              die = o[5]
            out = f'{o[0]}. {fixname(o[1])} born: {bor} died: {die}\n'
            out = re.sub('[+*]',' ',out)
            out = re.sub('  +',' ',out)
#            out = '{}. {]} born: {} died: {}\n'.format(o[0],o[1],o[2],o[3])
#            print (out)
            root.clipboard_append(out)  # append new value to clipboard
            temp[o[0]] = o


if __name__ == "__main__":
    root=tk.Tk()
    AhnMerge().callback1()
