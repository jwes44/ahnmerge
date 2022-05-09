

import tkinter as tk
import time
from geoutl import valname

 
if __name__ == "__main__":
    root=tk.Tk()
    lines = root.clipboard_get().splitlines()
    tic = time.perf_counter()
    for line in lines:
        b = valname(line)
        print(line)
        for a in b:
            print('    ',a)
    toc = time.perf_counter()
    print(f" {toc - tic:0.4f} seconds")
