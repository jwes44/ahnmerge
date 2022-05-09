#"x1":110.5425,"x2":507.5775,"y1":66.1725,"y2":548.8875
import tabula
import re

def pd(t):
    m = re.match(r"(.*[0-9-/.]{4,10} .*[0-9]{1,2}) (.*)", t)
    if m:
        died = m.group(2) + ', ' + m.group(1)
    else:
        m = re.match(r"(.*[0-9-/.]{4,10}) (.*)", t)
        if m:
            died = m.group(2) + ', ' + m.group(1)
        else:
            died = t
    return died

while True:
    df = tabula.read_pdf('C:/Users/j/Downloads/Pedigree View - Printer Friendly - Ancestry.com.pdf', output_format="json", lattice=True, pages=1, area=(68,110,564,507))
#    df = tabula.read_pdf('C:/Users/j/Downloads/Pedigree View - Printer Friendly - Ancestry.com.pdf', output_format="json", lattice=True, pages=1)
    #print(df)
    ahn = {0:[[300,0],[400,1]],1:[[300,2],[1000,3]],2:[[150,4],[300,5],[400,6],[1000,7]],3:[[95,8],[157,9],[221,10],[285,11],[347,12],[409,13],[473,14],[1000,15]],5:[[77,16],[115,17],[140,18],[178,19],[203,20],[241,21],[266,22],[304,23],[329,24],[367,25],[392,26],[430,27],[455,28],[493,29],[518,30],[1000,31]]}
    #ahn = {0:[[400,1]],1:[[300,2],[1000,3]]}
    ah = {}
    for i in range(len(df)):
        for j in range(len(df[i]['data'])):
            for k in range(len(df[i]['data'][j])):
                if df[i]['data'][j][k]['text']:
    #                print(df[i]['data'][j][k])
    #                print(i,j,k,'top {:6.2f} left {:6.2f} width {:6.2f} height {:6.2f}'.format(df[i]['data'][j][k]['top'],df[i]['data'][j][k]['left'],df[i]['data'][j][k]['width'],df[i]['data'][j][k]['height']))
                    col = int((df[i]['data'][j][k]['left']-111)/53)
                    if col in ahn:
                        for n in range(len(ahn[col])):
                            if df[i]['data'][j][k]['top'] < ahn[col][n][0]:
                                anum = str(ahn[col][n][1])
                                break
                    else:
                        anum = '0'
                    t = df[i]['data'][j][k]['text'].replace(':\r', ': ')
                    t = t.replace('\r', '')
                    t = t.replace('{', '(')
                    t = t.replace('}', ')')
                    t1  = t.split('D:')
                    if len(t1) > 1:
                        died = pd(t1[1])
                    else:
                        died = ''
                    t2  = t1[0].split('M:')
                    t3  = t2[0].split('B:')
                    if len(t3) > 1:
                        born = ' born: ' + pd(t3[1])
                    else:
                        born = ' born: '
                    out = '{}. ' + t3[0] + born + ' died: ' + died
                    out.replace('  ', ' ')
                    if int(anum) in ah:
                        ah[int(anum)] = ah[int(anum)] + ' ' + died
                    else:
                        ah[int(anum)] = out
#                    print(out.format(anum))
    for o in sorted(ah):
        print(ah[o].format(o))
    no = input("again?")
    if no == 'n':
        break
#'top': 286.24356,: 406.89944,: 90 ''.16305541992188, ''