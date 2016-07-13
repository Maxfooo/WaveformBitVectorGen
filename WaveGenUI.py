'''
Created on Apr 18, 2016
@author: maxr
'''

from tkinter import *
from SinusoidUI import SinusoidUI as sUI
from RampUI import RampUI as rUI
import tkinter.messagebox as mb
from PIL import ImageTk, Image

class WaveGenUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("Waveform Bit Vector Generator")
        self.pack()
        self.versionNumber = '1.0.0'
        self.initUI()

    def initUI(self):
        self.coverImage()
        self.waveformSelect()

    def coverImage(self):
        wfImage = Image.open("WaveformBitVectorGenerator.png")
        wfPhoto = ImageTk.PhotoImage(wfImage)
        self.wfLabel = Label(self, image=wfPhoto)
        self.wfLabel.image = wfPhoto
        self.wfLabel.pack(fill=BOTH)

    def waveformSelect(self):
        self.waveFormFrame = LabelFrame(self, text = 'Waveform Select')
        
        self.sineButton = Button(self.waveFormFrame, text = 'Sinusoid', command=self.sineUI)
        self.sineButton.pack(fill=BOTH)
        
        self.rampButton = Button(self.waveFormFrame, text = 'Ramp', command=self.rampUI)
        self.rampButton.pack(fill=BOTH)
        
        self.versionButton = Button(self.waveFormFrame, text = 'App Info', command=self.infoDialogbox)
        self.versionButton.pack(fill = BOTH)
        
        self.waveFormFrame.pack(fill=BOTH, expand=1)
        
        
    def sineUI(self):
        sineTop = Toplevel()
        sineApp = sUI(master = sineTop)
        sineApp.mainloop()
    

    def rampUI(self):
        rampTop = Toplevel()
        rampApp = rUI(master = rampTop)
        rampApp.mainloop()
        
    def infoDialogbox(self):
        mb.showinfo("Wavegen Information", "Author: Max A. Ruiz\nVersion: {}".format(self.versionNumber))



if __name__ == '__main__':
    root = Tk()
    root.geometry("300x200")
    app = WaveGenUI(master=root)
    app.mainloop()
