'''
Created on Apr 18, 2016

@author: maxr
'''

from tkinter import *
from GenerateSinusoid import GenerateSinusoid as gs
import tkinter.messagebox as mb

# EC = ERROR CODE
EC_WAVEFORM = 1
EC_BUSNAME = 2
EC_FILEBUFFERSIZE_HIGH = 3
EC_FILEBUFFERSIZE_LOW = 4
EC_FILEBUFFERSIZE_TYPE = 5
EC_BITRESOLUTION_HIGH = 6
EC_BITRESOLUTION_LOW = 7
EC_BITRESOLUTION_TYPE = 8


class WaveGenUI(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("Waveform Bit Vector Generator")
        self.pack()
        
        self.initUI()
        
    def initUI(self):
        self.waveformSelect()
        self.paramInput()
        self.generateButton()
        
    
    def waveformSelect(self):
        self.waveFormFrame = LabelFrame(self, text = 'Waveform Select')
        
        self.wvfVar = IntVar()
        
        
        self.sinRadiobutton = Radiobutton(self.waveFormFrame, padx=2,
                                          text = 'sinusoid', variable=self.wvfVar, value = 1)
        self.sinRadiobutton.pack()
        self.waveFormFrame.pack(fill=BOTH)
    
    def paramInput(self):
        self.paramFrame = LabelFrame(self, text='Parameter Input')
        
        self.busName = StringVar()
        self.fileBufferSize = StringVar()
        self.bitResolution = StringVar()
        
        self.bnFrame = Frame(self.paramFrame)
        bnLabel = Label(self.bnFrame, text = 'Bus Name', pady=4, padx = 4)
        bnLabel.pack(side = LEFT)
        bnEntry = Entry(self.bnFrame, textvariable = self.busName, width=15)
        bnEntry.pack(side = LEFT)
        self.bnFrame.pack(anchor = W)
        
        self.fbsFrame = Frame(self.paramFrame)
        fbsLabel = Label(self.fbsFrame, text = ' File Buffer Size', pady=4)
        fbsLabel.pack(side = LEFT)
        fbsEntry = Entry(self.fbsFrame, textvariable = self.fileBufferSize, width=12)
        fbsEntry.pack(side = LEFT)
        self.fbsFrame.pack(anchor = W)
        
        self.brFrame = Frame(self.paramFrame)
        brLabel = Label(self.brFrame, text = 'Bit Resolution', pady=4, padx = 4)
        brLabel.pack(side = LEFT)
        brEntry = Entry(self.brFrame, textvariable = self.bitResolution, width=12)
        brEntry.pack(side = LEFT)
        self.brFrame.pack(anchor = W)
        
        self.paramFrame.pack(fill=BOTH)
        
        self.busName.set("Bus_01")
        self.fileBufferSize.set("512")
        self.bitResolution.set("12")
        
    def generateButton(self):
        self.startGenFrame = LabelFrame(self, text='Generate Waveform')
        
        self.gbFrame = Frame(self.startGenFrame)
        genButton = Button(self.gbFrame, text = 'Begin', justify=CENTER, width=10, 
                           command = self.generateWaveform)
        genButton.pack()
        
        self.gbFrame.pack()
        
        self.startGenFrame.pack(fill=BOTH)
        
    def generateWaveform(self):
        error = []
        errorMessage = ''
        
        _wvfVar = self.wvfVar.get()
        if _wvfVar != 1:
            error.append(EC_WAVEFORM)
        
        _busName = self.busName.get()
        if len(_busName) == 0:
            error.append(EC_BUSNAME)
        
        try:
            _fbs = int(self.fileBufferSize.get())
            if int(_fbs) > 512:
                error.append(EC_FILEBUFFERSIZE_HIGH)
            elif int(_fbs) < 1:
                error.append(EC_FILEBUFFERSIZE_LOW)
        except:
            error.append(EC_FILEBUFFERSIZE_TYPE)
            
        try:
            _bitRes = int(self.bitResolution.get())
            if _bitRes > 12:
                error.append(EC_BITRESOLUTION_HIGH)
            elif _bitRes < 1:
                error.append(EC_BITRESOLUTION_LOW)
        except:
            error.append(EC_BITRESOLUTION_TYPE)
            
            
        if len(error) > 0:
            for i,err in enumerate(error):
                if err == EC_WAVEFORM:
                    errorMessage += "({}) Please select a waveform\n".format(i)
                elif err == EC_BUSNAME:
                    errorMessage += "({}) Please enter a bus name\n".format(i)
                elif err == EC_FILEBUFFERSIZE_HIGH:
                    errorMessage += "({}) File buffer size must be 512 or less\n".format(i)
                elif err == EC_FILEBUFFERSIZE_LOW:
                    errorMessage += "({}) File buffer size must be 1 or greater\n".format(i)
                elif err == EC_FILEBUFFERSIZE_TYPE:
                    errorMessage += "({}) File buffer size must be an integer\n".format(i)
                elif err == EC_BITRESOLUTION_HIGH:
                    errorMessage += "({}) Bit resolution must be 12 or less\n".format(i)
                elif err == EC_BITRESOLUTION_LOW:
                    errorMessage += "({}) Bit resolution must be 1 or greater".format(i)
                elif err == EC_BITRESOLUTION_TYPE:
                    errorMessage += "({}) Bit resolution must be an integer\n".format(i)
                else:
                    errorMessage += "Unknown error encountered\n"
                    
            mb.showinfo("Error", errorMessage)
        else:
            if _wvfVar == 1:
                _gs = gs(_busName, _fbs, _bitRes)
                _gs.run()
        
    
    
if __name__ == '__main__':
    root = Tk()
    root.geometry("200x200")
    app = WaveGenUI(master=root)
    app.mainloop()