
#"x1":110.5425,"x2":507.5775,"y1":66.1725,"y2":548.8875
import tabula
import re
import os
from tkinter import Tk, ttk, Text, IntVar, Menu, Scrollbar, INSERT, N, S, E, W, RIGHT, Y, END

from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfilename, askopenfilename


class RightClicker:
    def __init__(self, event):
        right_click_menu = Menu(None, tearoff=0, takefocus=0)

        for txt in ['Cut', 'Copy', 'Paste']:
            right_click_menu.add_command(
                label=txt, command=lambda event=event, text=txt:
                self.right_click_command(event, text))

        right_click_menu.tk_popup(event.x_root + 40, event.y_root + 10, entry='0')

    def right_click_command(self, event, cmd):
        event.widget.event_generate(f'<<{cmd}>>')


class Notepad:
    search_strings = [r'([0-9]*[13579]\..*) [^\W\d_]+ born:', r'\(.*\) ']
    repl_strings = [r'\1  born:']
    def __init__(self, **kwargs):
        self.file_name = None
        self.root = Tk()
        self.root.title("Parse_anc_pdf1")
        self.root.bind('<Return>',lambda event:self.callback())
        ttk.Button(self.root, text="Read PDF", command=self.callback).grid(row=0, column=0)
        ttk.Button(self.root, text="Copy to clip", command=self.callback1).grid(row=0, column=1)
        ttk.Label(self.root, text='Find', borderwidth="1", relief="solid").grid(row=0, column=2)
        self.find = ttk.Combobox(self.root)
        self.find.grid(row=0, column=3)
        self.find['values'] = self.search_strings
        ttk.Label(self.root, text='Replace with', borderwidth="1", relief="solid").grid(row=0, column=4)
        self.repl = ttk.Combobox(self.root)
        self.repl.grid(row=0, column=5)
        self.repl['values'] = self.repl_strings
        ttk.Button(self.root, text="Find next", command=self.callback2).grid(row=0, column=6, sticky='E')
        ttk.Button(self.root, text="Replace", command=self.callback3).grid(row=0, column=7, sticky='E')
        self.text_area = Text(self.root)

        self.text_area.bind('<Button-3>', RightClicker)

        # set icon and window size (default is 300 x 300)
        try:
            self.root.wm_iconbitmap("Notepad.ico")
        except:   #pylint: disable=W0702
            pass
        width = 1000
        height = 550
        # place notepad in the center of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        left = (screen_width / 2) - (width / 2)
        top = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, left, top))

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        for i in range(8):
            self.root.grid_columnconfigure(i, weight=1)

        self.text_area.grid(row=1, column=0, columnspan=8, sticky=N + E + S + W)

    def quit_application(self):
        self.root.destroy()

    def callback(self): 
        self.text_area.delete(1.0, END)
        self.text_area.insert(1.0, read_pdf())
        self.callback1()
        self.text_area.mark_set("insert", '1.0')

    def callback1(self): 
        self.root.clipboard_clear()  # clear clipboard contents
        self.root.clipboard_append(self.text_area.get(1.0, END))

    def callback2(self):
        self.text_area.tag_remove('found', '1.0', END)
        ser = self.find.get()
        length = IntVar() # num of matched chars
        if ser:
            if ser not in self.search_strings:
                self.search_strings.append(ser)
            alltext = str(self.text_area.get('1.0', END))
            c = self.text_area.count("1.0", INSERT, "chars")
            chars = c[0] if c else 0
            mo = re.search(ser, alltext[chars:])
            if mo:
                self.idx = self.text_area.index('1.0+{0}c'.format(mo.start(0)+chars))
#            self.idx = self.text_area.search(ser, self.text_area.index(INSERT), regexp=True, stopindex=END, count=length)
            if  self.idx: 	    
                matchEnd = '{0}+{1}c'.format(self.idx, mo.end(0)-mo.start(0))
#                matchEnd = '{0}+{1}c'.format(self.idx, length.get())
                self.text_area.tag_add('found', self.idx, matchEnd)
                self.text_area.tag_config('found', background='light gray')
                self.text_area.mark_set("insert", matchEnd)



    def callback3(self): 
        i = self.text_area.tag_nextrange('found', '1.0')
        if i:
            ser = self.find.get()
            rep = self.repl.get()
            if rep not in self.repl_strings:
                self.repl_strings.append(rep)
            t = self.text_area.get(i[0],i[1])
            r1 = re.sub(ser, rep, t)
            self.text_area.delete(i[0],i[1])
            self.text_area.insert(i[0],r1)
            self.text_area.tag_remove('found', '1.0', END)
            self.callback2()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def run_notepad(self):
        self.root.mainloop()


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

def read_pdf():
#    download_folder = os.path.expanduser("~")+"/Downloads/"
    df = tabula.read_pdf(os.path.expanduser("~")+'/Downloads/Pedigree View - Printer Friendly - Ancestry.com.pdf', output_format="json", lattice=True, pages=1, area=(68,110,564,507))
#    df = tabula.read_pdf('C:/Users/jwesley/Downloads/Pedigree View - Printer Friendly - Ancestry.com.pdf', output_format="json", lattice=True, pages=1, area=(68,110,564,507))
#    df = tabula.read_pdf('C:/Users/jwesley/Downloads/Pedigree View - Printer Friendly - Ancestry.com.pdf', output_format="json", lattice=True, pages=1)
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
    oo = []
    for o in sorted(ah):
        oo.append(ah[o].format(o))
    return '\n'.join(oo)

#'top': 286.24356,: 406.89944,: 90 ''.16305541992188, ''
def main():
    notepad = Notepad(width=600, height=400)
    notepad.run_notepad()


if __name__ == '__main__':
    main()
