##Handle the Tkinter window, setting resolution.

from tkinter import *

class Window():
    def __init__(self,fullscreen=False):
        self.root = Tk()
        self.root.configure(background="black")
        self.root.focus_set()
        self.root.bind("<Escape>", quit)
        self.root.overrideredirect(1)
        if fullscreen:
            w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
            self.w = w
            self.h = h
            self.root.geometry(str(w)+"x"+str(h))            
    def run(self):
        self.root.mainloop()
