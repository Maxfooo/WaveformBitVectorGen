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
        
        self.waveFormFrame.pack(fill=BOTH, expand=1)
        
        
    def sineUI(self):
        sineTop = Toplevel()
        sineApp = sUI(master = sineTop)
        sineApp.mainloop()
    

    def rampUI(self):
        rampTop = Toplevel()
        rampApp = rUI(master = rampTop)
        rampApp.mainloop()



if __name__ == '__main__':
    root = Tk()
    root.geometry("300x180")
    app = WaveGenUI(master=root)
    app.mainloop()
