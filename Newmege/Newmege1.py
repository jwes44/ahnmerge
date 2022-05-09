
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import simpledialog
import re
import os
from ahnutl import nmb,pa
#from geoutl import valname

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def addline(ahn, n, a, f=False):
    def nti(l1,s,i):
        pnb = re.compile(r'[^ ,.]')
        if pnb.search(s):
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
#        b = valname(a.birthplace)
#        print (a.num,a.birthplace,b)
        nti(ahn[n][1],a.birthplace,f)
    except IndexError:
        pass
    try:
        nti(ahn[n][2],a.birthdate,f)
    except IndexError:
        pass
    try:
        nti(ahn[n][3],a.deathplace,f)
    except IndexError:
        pass
    try:
        nti(ahn[n][4],a.deathdate,f)
    except IndexError:
        pass

def parseahn(ahn, lines, off=1):
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

class AhnGUI:
    ahn = {}
    wig = []
    wids = [7,25,39,11,39,11]
    wids1 = [7,28,42,14,42,14]
    weights = [0,1,1,0,1,0]
    rows = 0
    maxrows = 0
    firstrow = 0
    keys = None
    def __init__(self,top,hxw):
        self.top = top
        self.hxw=hxw
        top.wm_title("Ahnmerge")
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
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
#        self.topFrame = tk.Frame(self.top, height=25, background="#7fffff")                    #place a frame on the canvas, this frame will hold the child widgets 
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
#        self.labelFrame = tk.Frame(self.top, height=25, borderwidth=3, background="#3fffff")                    #place a frame on the canvas, this frame will hold the child widgets 
        self.labelFrame.grid(row=1,column=0, sticky="NEW")       #place a frame on the canvas, this frame will hold the child widgets 
        self.labelFrame.grid_rowconfigure(0, weight=0)
#        self.labelFrame.grid_columnconfigure(0, weight=1)
        for col in range(len(labs)):
            ttk.Label(self.labelFrame, text=labs[col], width=self.wids1[col], borderwidth="1", 
                     relief="solid").grid(row=0, column=col, sticky="NEWS")
            self.labelFrame.grid_columnconfigure(col,weight=self.weights[col])
#        tk.Canvas(self.labelFrame, width=13,height=20).grid(row=0, column=6, sticky="EW")
        self.labelFrame.grid_columnconfigure(6,weight=0)
        self.bFrame = tk.Frame(self.top, background="#ffffff")
        self.bFrame.grid(row=2,column=0, sticky="NEWS")                
        self.bFrame.grid_columnconfigure(0, weight=1)
        self.botFrame = tk.Frame(self.bFrame, background="#ffffff")
        self.botFrame.grid(row=0,column=0, sticky="NEWS")                
        self.botFrame.grid_columnconfigure(0, weight=1)
        self.scroll = tk.Scrollbar(self.top, command=self.yview)
        self.scroll.grid(row=2,column=1, sticky="NS")   
        self.top.bind("<Configure>", self.onFrameConfigure)                       #bind an event whenever the size of the viewPort frame changes.

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
        return int((wh-43)/21)

    def scrollset(self, *args):
        print("Canvas",args)

    def yview(self, *args):
        self.scroll_rows = self.get_scroll_rows()
        self.scroll_len = float(self.scroll_rows)/len(self.keys)
        if self.scroll_rows < len(self.keys):
            print(args)
            if args[0] == 'moveto':
                self.scroll_pos = int(float(args[1])*len(self.keys))
                print(self.scroll_pos)
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
    
    def printMsg(self, msg):
        print(msg)

    def clickFunction(self, event): #event is argument with info about event that triggered the function
        self.sv.set(int(event.widget.cget("text"))) #event.widget is reference to widget that was clicked on and triggered the function 

    def rclickFunction(self, event): #event is argument with info about event that triggered the function
        self.callback4(event.widget.cget("text")) #event.widget is reference to widget that was clicked on and triggered the function 

    def dclickFunction(self, event): #event is argument with info about event that triggered the function
        self.callback5(int(event.widget.cget("text"))) #event.widget is reference to widget that was clicked on and triggered the function 

    def showahn(self):
        def newselection(event, other):
            other[event.widget.key][event.widget.x1][0], other[event.widget.key][event.widget.x1][event.widget.current()] = other[event.widget.key][event.widget.x1][event.widget.current()], other[event.widget.key][event.widget.x1][0]
        self.keys = sorted(self.ahn)
        root.wm_title(f"Ahnmerge {len(self.keys)}")
        self.scroll_rows = self.get_scroll_rows()
        i1 = self.rows
        self.rows =  min(self.scroll_rows, len(self.keys))
        if i1 < self.rows:
            for i2 in range(i1,self.rows):        
                self.botFrame.grid_rowconfigure(i2, weight=0)
                self.cbos.append([])
                self.labs.append([])
                tkl = ttk.Label(self.botFrame, anchor="e", width=7, borderwidth="1", relief="solid")
                tkl.grid(row=i2, column=0, sticky="NEWS")
                tkl.bind("<Button-1>", self.clickFunction)
                tkl.bind("<Double-Button-1>", self.dclickFunction)
                tkl.bind("<Button-3>", self.rclickFunction)
                self.botFrame.grid_columnconfigure(0, weight=self.weights[0])
                self.lns.append(tkl)

                for col in range(1,6):
                    self.botFrame.grid_columnconfigure(col, weight=self.weights[col])
                    tkc = ttk.Combobox(self.botFrame, state="readonly", width=self.wids[col])
                    tkc.grid(row=i2, column=col, sticky="NEWS")
                    tkc.bind("<<ComboboxSelected>>", lambda event:newselection(event, self.ahn))
                    tkl = ttk.Label(self.botFrame, width=self.wids[col]+3, borderwidth="1", relief="solid")
                    tkl.grid(row=i2, column=col, sticky="NEWS")
                    self.cbos[i2].append(tkc)
                    self.labs[i2].append(tkl)
        elif i1 > self.rows:
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
            tkw = self.lns[x]
            tkw.grid()
            tkw.lift()
            tkw.configure(text=str(self.keys[x+off]))
            y = self.ahn[self.keys[x+off]]
            for x1 in range(5):
                if len(y[x1]) <= 1:
                    tkl = self.labs[x][x1]
                    tkl.configure(text=y[x1][0] if len(y[x1]) else '')
                    tkl.grid()
                    tkl.lift()
                else:
                    tkc = self.cbos[x][x1]
                    tkc['values'] = y[x1]
                    tkc.set(y[x1][0])
                    tkc.grid()
                    tkc.lift()
                    self.cbos[x][x1].key = self.keys[x+off]
                    self.cbos[x][x1].x1 = x1
                    self.cbos[x][x1].bind("<<ComboboxSelected>>", lambda event:newselection(event, self.ahn))

    def callback(self):
        root.config(cursor="wait")
        lines = root.clipboard_get().splitlines()
        off = int(self.sv.get())
        parseahn(self.ahn, lines, off)
        self.showahn()
        root.config(cursor="")
#            print (self.keys[x+self.scroll_pos],self.ahn[self.keys[x+self.scroll_pos]])
    def callback2(self):
        global root
        self.ahn.clear()
        self.sv.set(1)
        self.cbvar.set(0)
        hxw = root.geometry()
        root.destroy()
        iinit(hxw)
        root.mainloop()

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
        if bool(self.cbvar.get()):
            for i in temp:
              t =  str(int(int(i)/2))
              if t in temp:
                if len(temp[t][3]) and len(temp[i][3]):
                  b1 = int(temp[t][3])
                  b2 = int(temp[i][3])
                  if b1 < b2 + 10 :
                    print(temp[i],'-',temp[t])

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
