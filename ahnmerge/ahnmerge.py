
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

# ************************
# Scrollable Frame Class
# ************************
class ScrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")          #place canvas on self
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview) #place a scrollbar on self 
        self.canvas.configure(yscrollcommand=self.vsb.set)                          #attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")                                       #pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)                     #pack canvas to left of self and expand to fil
        self.canvas.create_window((4,4), window=self.viewPort, anchor="nw",            #add view port frame to canvas
                                  tags="self.viewPort")

        self.viewPort.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.

    def onFrameConfigure(self, event):                                              
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))                 #whenever the size of the frame changes, alter the scroll region respectively.


# ********************************
# Example usage of the above class
# ********************************

class AhnMerge(tk.Frame):
    ahn = {}
    wig = []
    wids = [25,39,11,39,11]
    wids1 = [7,28,42,14,42,14]
    def __init__(self, root):
        tk.Frame.__init__(self, root) #set up a frame for buttons and headers
        self.sv = tk.StringVar()
        self.cbvar = tk.IntVar()
        labs = ["No. ","        Name        ","Birth Place","Birth Date","Death  Place","Death Date"]
        self.topFrame = tk.Frame(self, height=50, borderwidth=3, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.topFrame.pack(side="top", fill="both", expand=False)       #place a frame on the canvas, this frame will hold the child widgets 
        ttk.Label(self.topFrame, text='Paste into no.', width=13, borderwidth="1", 
                 relief="solid").grid(row=0, column=len(labs)-2, sticky='W')
        c = ttk.Checkbutton(self.topFrame, 
            text="Caps date",
            variable=self.cbvar).grid(row=0, column=1)
        self.mysb=tk.Spinbox(self.topFrame, textvariable=self.sv, from_=1, to=999,width=4, borderwidth=3).grid(row=0, column=len(labs)-2)
        ttk.Button(self.topFrame, text="Paste ahn from clip", command=self.callback).grid(row=0, column=len(labs)-2, sticky='E')
        ttk.Button(self.topFrame, text="Clear", width=6.5, command=self.callback2).grid(row=0, column=0)
        ttk.Button(self.topFrame, text="Copy ahn to clip", command=lambda: self.callback1(0)).grid(row=0, column=2)
        ttk.Button(self.topFrame, text="Help", command=self.callback3).grid(row=0, column=len(labs)-1)
        for col in range(len(labs)):
            ttk.Label(self.topFrame, text=labs[col], width=self.wids1[col], borderwidth="1", 
                     relief="solid").grid(row=1, column=col)
            self.grid_columnconfigure(col,weight=1)
        # when packing the scrollframe, we pack scrollFrame itself (NOT the viewPort)
        self.botFrame = tk.Frame(self, background="#ffffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.botFrame.pack(side="top", fill="both", expand=True)                   #place a frame on the canvas, this frame will hold the child widgets 
        self.scrollFrame = ScrollFrame(self.botFrame) # add a new scrollable frame.
        # Now add some controls to the scrollframe. 
        # NOTE: the child controls are added to the view port (scrollFrame.viewPort, NOT scrollframe itself)
        self.scrollFrame.pack(side="top", fill="both", expand=True)
    
    def printMsg(self, msg):
        print(msg)

    def clickFunction(self, event): #event is argument with info about event that triggered the function
        self.sv.set(int(event.widget.cget("text"))) #event.widget is reference to widget that was clicked on and triggered the function 

    def rclickFunction(self, event): #event is argument with info about event that triggered the function
        self.callback4(event.widget.cget("text")) #event.widget is reference to widget that was clicked on and triggered the function 

    def showahn(self):
        def newselection(event, other):
            other[event.widget.key][event.widget.x1][0], other[event.widget.key][event.widget.x1][event.widget.current()] = other[event.widget.key][event.widget.x1][event.widget.current()], other[event.widget.key][event.widget.x1][0]
        row = 2
        for wid in self.wig:
            wid.destroy()
        self.wig.clear()
        keys =sorted(self.ahn)
        root.wm_title(f"Ahnmerge {len(keys)}")
#        self.wids = [25,50,50]
        for x in range (len(keys)):
            tkw = ttk.Label(self.scrollFrame.viewPort, text=str(keys[x]), anchor="e", width=7, borderwidth="1", relief="solid")
            tkw.grid(row=row, column=0)
            tkw.bind("<Button-1>", self.clickFunction)
            tkw.bind("<Button-3>", self.rclickFunction)
            self.wig.append(tkw)
            y = self.ahn[keys[x]]
            for x1 in range(5):
                if len(y[x1]) <= 1:
                    tkw = ttk.Label(self.scrollFrame.viewPort, text=y[x1][0] if len(y[x1]) else '', width=self.wids[x1]+3, borderwidth="1", relief="solid")
                else:
                    tkw = ttk.Combobox(self.scrollFrame.viewPort, values=y[x1], state="readonly", width=self.wids[x1])
                    tkw.set(y[x1][0])
                tkw.grid(row=row, column=x1+1)
                self.wig.append(tkw)
                if len(y[x1]) > 1:
                    self.wig[len(self.wig)-1].key = keys[x]
                    self.wig[len(self.wig)-1].x1 = x1
                    self.wig[len(self.wig)-1].bind("<<ComboboxSelected>>", lambda event:newselection(event, self.ahn))
            row=row+1

    def callback(self):
        root.config(cursor="wait")
        lines = root.clipboard_get().splitlines()
        off = int(self.sv.get())
        parseahn(self.ahn, lines, off)
        self.showahn()
        root.config(cursor="")
#            print (keys[x],self.ahn[keys[x]])

    def callback2(self):
        for wid in self.wig:
            wid.destroy()
        self.wig.clear()
        self.ahn.clear()
        self.sv.set(1)
        self.cbvar.set(0)
        root.wm_title("Ahnmerge")
    def callback3(self):
        messagebox.showinfo(
            "Ahnentafel merge help",
            "This is help"
            )
    def callback4(self,num):
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
                n = n.title()
#                n = re.sub(' i*[iv] ', ' ', n, flags=re.IGNORECASE)
                n = re.sub('\.', '', n)
                n = re.sub('__+', '', n)
                if bool(self.cbvar.get()):
                    ll = n.split()
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
        temp = {}
        for line in range(0,len(self.wig),6):
            o = []
            for i in range(line,line+6):
                if 'label' in str(self.wig[i]):
                    o.append(self.wig[i].cget("text").strip(', '))
                else:
                    o.append(self.wig[i].get().strip(', '))
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
        if bool(self.cbvar.get()):
            for i in temp:
              t =  str(int(int(i)/2))
              if t in temp:
                if len(temp[t][3]) and len(temp[i][3]):
                  b1 = int(temp[t][3])
                  b2 = int(temp[i][3])
                  if b1 < b2 + 10 :
                    print(temp[i],'-',temp[t])


if __name__ == "__main__":
    root=tk.Tk()
    root.wm_title("Ahnmerge")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    hxw='{0:d}x{1:d}'.format(min(940,screen_width),min(560,screen_height))
    root.geometry(hxw) #Width x Height
    AhnMerge(root).pack(side="top", fill="both", expand=True)
    root.mainloop()