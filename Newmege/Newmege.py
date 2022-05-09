
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import simpledialog
import re
import os
#from ahnutl import nmb,pa
from geoutl import valname, geoclear

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


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
        s = pcm.sub(', ',s)
        s = s.translate(trantab)    # `change curly quotes to straight
        s = re.sub('\.\.\.', '…', s)
        s = re.sub('\.', '', s)
        s = re.sub('__+', '', s)
        ll = s.split()
        for i in range(len(ll)):
            if re.search('[A-Z]{2}', ll[i]) or not re.search('[A-Z]', ll[i]):
                ll[i] = ll[i].title()
        return s

    def fixn(s):
        s = fix1(s)
        if s:
            ll = s.split()
            for i in range(len(ll)):
                if re.search('[A-Z]{2}', ll[i]) or not re.search('[A-Z]', ll[i]):
                    ll[i] = ll[i].title()
            s = ' '.join(ll)
        return s

    def fixpl(s):
        s = fix1(s)
        s = s.strip(", ")
        if s:
            ll = s.split(', ')
            pl = ll[len(ll)-1].split('…')
            if len(pl[0]) > 2 and 'united states of america'.startswith(pl[0].lower()):
                ll[len(ll)-1] = 'USA'
            s = ', '.join(ll)
        return s

#This tries to put all dates in a format day month year 
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
#            print(pla,m)
            return [pla,m.group(0)]
        if baddate:
            return ['Bad date',pad]
        pla = pad[:dend].strip(", ")
#            print(pla,m)
        if mo in mdict:
            mo = mdict[mo]
#            print(str(day) + ' ' +  + ' ' + m.group(1))
        return [pla,str(day) + ' ' + mo + ' ' + yr]
    xx = nmb()
    a1=p.split(line)
    if len(a1) < 3:
#        print(line)
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

    xx.name = fixn(name)
#        print(plda)
    try:
        xx.birthplace = fixpl(str(plda[0][0]))
    except IndexError:
        pass
    try:
        xx.birthdate = fix1(str(plda[0][1]))
    except IndexError:
        pass
    try:
        xx.deathplace = fixpl(str(plda[1][0]))
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
pddd = re.compile(r' *\*+ *')
psp = re.compile(r'  +')
pcm = re.compile(r' *, *')
p = re.compile(r' born: ?| ?died: ?')
p1 = re.compile(r'\. ')
# pdate is a list of date formats to be converted to DD Mon YYYY
#  0 - Between date, date
#  1 - Month Day[,] Year
#  2 - MM[-/]DD[-/]YYYY or DD[-/]MM[-/]YYYY if month os out of range
#  3 - YYYY[-/]MM[-/]DD
#  4 - DD[ -/]Month[ -/]YYYY
#  5 - Month[ -/]YYYY
#  6 - YYYY
pdate = \
[re.compile(r'((Betw?\.?)|(Between)).*([0-9]{4}).*([0-9]{4})'),
re.compile(r'([^\W\d_]{3,})[,. ]+([0-9]{1,2})[, ]+([0-9]{4})'),
re.compile(r'([0-9]{1,2})[-/. ]([0-9]{1,2})[-/. ]([0-9]{4})'),
re.compile(r'([0-9]{4})[-/]([0-9]{1,2})[-/]([0-9]{1,2})'),
re.compile(r'([0-9]{1,2})[ -/]?([^\W\d_]{3,})[.,]?[ -/]?([0-9]{4})'),
re.compile(r'([^\W\d_]{3,})\.? ([0-9]{4})'),
re.compile(r'([0-9]{1,2})[ -/]([0-9]{4})'),
re.compile(r'([0-9]{4})[, ]*$')]
pnb = re.compile(r'[^ ,.]')

def addline(ahn, n, a, f=False):
#This adds an item to a list for a combo box
    def nti(l1,s,i):
        if (i and l1) or pnb.search(s):
            s = s.strip(", ")
            if s in l1:
                return
            if i:
                l1.insert(0,s)
            else:
                l1.append(s)
    if n not in ahn:
        ahn[n] = [[],[],[],[],[]]
    nti(ahn[n][0],a.name,f)
#            print(plda)
    try:
        if a.birthplace:
            b = valname(a.birthplace,root)
        else:
            b = ''
#        print (a.num,a.birthplace,b)
        nti(ahn[n][1],b,f)
    except IndexError:
        pass
    try:
        nti(ahn[n][2],a.birthdate,f)
    except IndexError:
        pass
    try:
        if a.deathplace:
            b = valname(a.deathplace,root)
        else:
            b = ''
        nti(ahn[n][3],b,f)
    except IndexError:
        pass
    try:
        nti(ahn[n][4],a.deathdate,f)
    except IndexError:
        pass

def parseahn(ahn, lines, off=1):
#This parses an Ahnentafel into a list of Records
    r = False
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
        addline(ahn, num,ao)
        r = True
    return r
g = []
di = []

class AhnGUI:
    ahn = {}    #key is #, and entry is a list of 5 lists - name, birthdate, birthplace, deathdate, deathplace
    wids = [7,25,39,11,39,11]
    wids1 = [7,28,42,14,42,14]
    weights = [0,1,1,0,1,0]
    rows = 0
    maxrows = 0
    firstrow = 0
    keys = None
    def __init__(self,top,hxw): # hxw is used to restore screen to previous location after clear
        self.top = top
        self.hxw=hxw
        top.wm_title("Ahnmerge")
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        self.maxrows = int((screen_height-43)/21)
#        for i in range(int(screen_height/25))
        if not self.hxw:
            self.hxw='{0:d}x{1:d}+{2:d}+{3:d}'.format(min(940,screen_width),min(560,screen_height),int(screen_width/3),int(screen_height/3))
        self.top.geometry(self.hxw) #Width x Height
        top.configure(bd=2)
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_rowconfigure(0, weight=0)
        self.top.grid_rowconfigure(1, weight=0)
        self.top.grid_rowconfigure(2, weight=1)
        self.sv = tk.StringVar()
        self.cbvar = tk.IntVar()
        self.h = 560
        self.cbos = []
        self.labs = []
        self.lns = []
        self.scroll_pos = 0
        labs = ["No.","Name","Birth Place","Birth Date","Death  Place","Death Date"]
        self.topFrame = tk.Frame(self.top, height=25, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.topFrame.grid(row=0,column=0, sticky="NEW")       #place a frame on the canvas, this frame will hold the child widgets 
        ttk.Button(self.topFrame, text="Clear", width=6.5, command=self.callback2).grid(row=0, column=0)
        c = ttk.Checkbutton(self.topFrame, text="Caps date", variable=self.cbvar).grid(row=0, column=1)
        ttk.Button(self.topFrame, text="Copy ahn to clip", command=lambda: self.callback1(0)).grid(row=0, column=2)
        ttk.Button(self.topFrame, text="Paste ahn from clip", command=self.callback).grid(row=0, column=3, sticky='E')
        ttk.Label(self.topFrame, text='Paste into no.', width=13, borderwidth="1", 
                 relief="solid").grid(row=0, column=4, sticky='E')
        self.mysb=tk.Spinbox(self.topFrame, textvariable=self.sv, from_=1, to=999,width=4).grid(row=0, column=5, sticky='W')
        ttk.Button(self.topFrame, text="Help", command=self.callback3).grid(row=0, column=6, sticky='E')
        for i in range(7):
            self.topFrame.grid_columnconfigure(i, weight=1)
        self.labelFrame = tk.Frame(self.top, height=25, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.labelFrame.grid(row=1,column=0, sticky="NEW")       #place a frame on the canvas, this frame will hold the child widgets 
        self.labelFrame.grid_rowconfigure(0, weight=0)
        for col in range(len(labs)):
            ttk.Label(self.labelFrame, text=labs[col], width=self.wids1[col], borderwidth="1", 
                     relief="solid").grid(row=0, column=col, sticky="NEWS")
            self.labelFrame.grid_columnconfigure(col,weight=self.weights[col]) # set so Birth Date, Death Date do not change width
        self.labelFrame.grid_columnconfigure(6,weight=0)
        self.bFrame = tk.Frame(self.top, background="#ffffff")
        self.bFrame.grid(row=2,column=0, sticky="NEWS")                
        self.bFrame.grid_columnconfigure(0, weight=1)
        self.botFrame = tk.Frame(self.bFrame, background="#ffffff")
        self.botFrame.grid(row=0,column=0, sticky="NEWS")                
        self.botFrame.grid_columnconfigure(0, weight=1)
        self.scroll = tk.Scrollbar(self.top, command=self.yview)    #scrolling is faked locally 
        self.scroll.grid(row=2,column=1, sticky="NS")   
        self.top.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.
        for i2 in range(self.maxrows):        #configure grid of widgets and make them invisible
            self.botFrame.grid_rowconfigure(i2, weight=0)
            self.cbos.append([])
            self.labs.append([])
            tkl = ttk.Label(self.botFrame, anchor="e", width=7, borderwidth="1", relief="solid")
            zzz = tkl._root().cget('bg')
            tkl.grid(row=i2, column=0, sticky="NEWS")
            tkl.bind("<Button-1>", self.clickFunction)
            tkl.bind("<Double-Button-1>", self.dclickFunction)
            tkl.bind("<Button-3>", self.rclickFunction)
            self.botFrame.grid_columnconfigure(0, weight=self.weights[0])
            tkl.grid_remove()
            self.lns.append(tkl)

            for col in range(1,6):
                self.botFrame.grid_columnconfigure(col, weight=self.weights[col])
                tkc = ttk.Combobox(self.botFrame, state="readonly", width=self.wids[col])
                tkc.grid(row=i2, column=col, sticky="NEWS")
                tkc.bind("<<ComboboxSelected>>", lambda event:newselection(event, self.ahn))
                tkc.grid_remove()
                tkl = ttk.Label(self.botFrame, width=self.wids[col]+3, borderwidth="1", relief="solid")
                tkl.grid(row=i2, column=col, sticky="NEWS")
                tkl.grid_remove()
                self.cbos[i2].append(tkc)
                self.labs[i2].append(tkl)

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        if self.keys and (self.scroll_rows <= len(self.keys)):
            i = self.get_scroll_rows()
            if i != self.scroll_rows:
                self.scroll_rows = i
                self.showahn()
#                print(event,'---',self.scroll_rows, len(self.keys))
        
    def get_scroll_rows(self):
        wh = self.top.winfo_height()
        xxh = self.lns[0].winfo_height()
        if xxh < 10:
            xxh = 19
        return int((wh-43)/xxh)


#
    def yview(self, *args):     #due to tk resource constraints, scrolling is faked locally
        self.scroll_rows = self.get_scroll_rows()
        self.scroll_len = float(self.scroll_rows)/len(self.keys)
        if self.scroll_rows < len(self.keys):
#            print(args)
            if args[0] == 'moveto':
                self.scroll_pos = int(float(args[1])*len(self.keys))
#                print(self.scroll_pos)
            elif args[0] == 'scroll':
                if args[2] == 'units':
                    t1 = int(args[1])
                if args[2] == 'pages':
                    t1 = int(args[1])*(self.scroll_rows-1)
                self.scroll_pos  += t1
                if self.scroll_pos < 0:
                    self.scroll_pos =  0
            self.showahn()
 #               print('SET',t, t + self.scroll_len)

#       set next paste to # clicked on
    def clickFunction(self, event): #event is argument with info about event that triggered the function
        self.sv.set(int(event.widget.cget("text"))) #event.widget is reference to widget that was clicked on and triggered the function 

#        offer to delete a person and his ancestors
    def rclickFunction(self, event): #event is argument with info about event that triggered the function
        self.callback4(event.widget.cget("text")) #event.widget is reference to widget that was clicked on and triggered the function 

#       edit a person
    def dclickFunction(self, event): #event is argument with info about event that triggered the function
        self.callback5(int(event.widget.cget("text"))) #event.widget is reference to widget that was clicked on and triggered the function 

    def showahn(self):  # shows the part of the ` that fits in the window
        def newselection(event, other): # exchanges data in the ` list when a selection is made in a combobox
            other[event.widget.key][event.widget.x1][0], other[event.widget.key][event.widget.x1][event.widget.current()] = other[event.widget.key][event.widget.x1][event.widget.current()], other[event.widget.key][event.widget.x1][0]
        self.keys = sorted(self.ahn)
        root.wm_title(f"Ahnmerge {len(self.keys)}")
        self.scroll_rows = self.get_scroll_rows()
        i1 = self.rows
        self.rows =  min(self.scroll_rows, len(self.keys))
        if i1 > self.rows:
            for i2 in range(self.rows,i1):        
                tkw = self.lns[i2]
                tkw.grid_remove()
                for col in range(5):
                    tkl = self.labs[i2][col]
                    tkc = self.cbos[i2][col]
                    tkl.grid_remove()
                    tkc.grid_remove()

        self.scroll_len = float(self.scroll_rows)/len(self.keys)
        if self.scroll_rows + 1 >= len(self.keys):
            self.scroll.set(0.0,1.0)
            t = 0.0
        else:
            if self.scroll_pos >=  len(self.keys) - self.scroll_rows:
                self.scroll_pos =  len(self.keys) - self.scroll_rows
                self.scroll.set(1.0 - self.scroll_len, 1.0)
                t = 1.0 - self.scroll_len
            else:
                t = self.scroll_pos/float(len(self.keys))
                self.scroll.set(t, t + self.scroll_len)
#        self.bCanvas.yview('moveto', '0.2')
        off = self.scroll_pos
        for x in range (self.rows):
#           This is to mark people that don't have two ancestors
            ahnn = self.keys[x+off]
            if 2*ahnn not in self.ahn or 2*ahnn+1 not in self.ahn:
                bgc = 'CadetBlue1'
            else:
                bgc = 'SystemButtonFace'
            tkw = self.lns[x]
            tkw.grid()
#            tkw.lift()
            tkw.configure(text=str(self.keys[x+off]), background = bgc)
            y = self.ahn[self.keys[x+off]]
            for x1 in range(5):
                if len(y[x1]) <= 1: # 0-1 entries, use a Label widget
                    tkl = self.labs[x][x1]
                    tkl.configure(text=y[x1][0] if len(y[x1]) else '')
                    tkl.grid()
                    tkl.lift()
                else: # 2+ entries, use a Combobox widget
                    tkc = self.cbos[x][x1]
                    tkc['values'] = y[x1]
                    tkc.set(y[x1][0])
                    tkc.grid()
                    tkc.lift()
                    self.cbos[x][x1].key = self.keys[x+off]
                    self.cbos[x][x1].x1 = x1
                    self.cbos[x][x1].bind("<<ComboboxSelected>>", lambda event:newselection(event, self.ahn))
#            root.update_idletasks()

    def callback(self): # paste ` from clipboard
        root.config(cursor="wait")
        lines = root.clipboard_get().splitlines()
        off = int(self.sv.get())
        if parseahn(self.ahn, lines, off):
            self.showahn()
        root.config(cursor="")

    def callback2(self):    # destroy and create the Tk window
        global root
        self.ahn.clear()
        self.sv.set(1)
        self.cbvar.set(0)
        hxw = root.geometry()
        root.destroy()
        iinit(hxw)
        geoclear()
        root.mainloop()

    def callback3(self):
        messagebox.showinfo(
            "Ahnentafel merge help",
            "This program allows you to merge `s"
            )

    def callback4(self,num):    # Delete person and all his ancestors
        def delt(num):
          if num in self.ahn:
              del self.ahn[num]
              delt(2*num)
              delt(2*num+1)
#        print(self.ahn[int(num)])
        try:
            dname = self.ahn[int(num)][0][0]
        except IndexError:
            dname = str(num)
        if messagebox.askyesno("Delete", f"Delete person {dname} and all ancestors?"):
            delt(int(num))
            self.showahn()

    def callback1(self,ty):
        def fixname(n):
            if n:
                n = re.sub('\.', '', n)
                n = re.sub('__+', '', n)
                ll = n.split()
#                n = re.sub(' i*[iv] ', ' ', n, flags=re.IGNORECASE)
                if bool(self.cbvar.get()):
                    for i in range(len(ll)-1, 0, -1):
                        if len(ll[i]) > 2:
                            if ll[i] in ['Rev', 'Pvt', 'Cpl', 'Sgt', 'Capt', 'Iii']:
                                continue
                            ll[i] = ll[i].upper()
                            break
                n = ' '.join(ll)
            return n
        def fxdate(n):
            if bool(self.cbvar.get()):
                m = re.search('[0-9]{4}',n)
                if m:
                    n = m.group(0)
            return n
        root.clipboard_clear()  # clear clipboard contents
        cls()
        line = 0
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

    def callback5(self,num):
        if num in self.ahn:
            y = self.ahn[num]
            o = [num]
            for i in range(5):
                o.append(y[i][0] if y[i] else '')
            if o[2]:
              bor = f'{o[2]}, {o[3]}'
            else:
              bor = o[3]
            if o[4]:
              die = f'{o[4]}, {o[5]}'
            else:
              die = o[5]
            out = f'{o[0]}. {o[1]} born: {bor} died: {die}\n'
            out = re.sub('[+*]',' ',out)
            out = re.sub('  +',' ',out)
            USER_INP = simpledialog.askstring(title="Edit", prompt="",initialvalue=out,parent=root)
            if USER_INP:
                l = pa(USER_INP)
                addline(self.ahn, l.num, l, True)
                self.showahn()
        return

def iinit(hxw):
    global root
    root=tk.Tk()
    root.iconphoto(False, tk.PhotoImage(file='newmerge.png'))
    AhnGUI(root,hxw)

if __name__ == "__main__":
    iinit(None)
    root.mainloop()
