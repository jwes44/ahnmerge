import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
from geoutl import valname

class gui:
    def __init__(self,top):
        top.wm_title("Geonames")
        self.topFrame = tk.Frame(root)                    #place a frame on the canvas, this frame will hold the child widgets 
        self.topFrame.grid(row=0,column=0, sticky="NEW")       #place a frame on the canvas, this frame will hold the child widgets 
        ttk.Button(self.topFrame, text="Search", width=6.5, command=self.callback).grid(row=0, column=1)
        self.v = tk.StringVar()
        self.e = tk.Entry(self.topFrame, width=65, textvariable=self.v)
        self.e.grid(row=0, column=0)
        self.e.bind("<Button-3>", self.rclickFunction)
        scrollbar = tk.Scrollbar(self.topFrame, orient=tk.VERTICAL)
        self.lb = tk.Listbox(self.topFrame, width=100, yscrollcommand=scrollbar.set)
        self.lb.grid(row=1, column=0)
        scrollbar.config(command=self.lb.yview)
        scrollbar.grid(row=1, column=1, sticky='NES')

    def rclickFunction(self, event): #event is argument with info about event that triggered the function
        event.widget.delete(0, tk.END) #event.widget is reference to widget that was clicked on and triggered the function 
        event.widget.insert(0, root.clipboard_get()) #event.widget is reference to widget that was clicked on and triggered the function 

    def callback(self):

        self.lb.delete(0, tk.END)
        o = valname(self.v.get())
        for item in o:
            self.lb.insert(tk.END, item)
        return

if __name__ == "__main__":
#    source = sqlite3.connect('e:/geonames.db')
#    dest = sqlite3.connect(':memory:')
#    source.backup(dest)
    root=tk.Tk()
    GUI=gui(root)
    root.mainloop()

