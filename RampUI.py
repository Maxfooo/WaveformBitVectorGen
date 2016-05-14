'''
Created on May 12, 2016

@author: maxr
'''
from tkinter import *
from GenerateRamp import GenerateRamp as gr
import tkinter.messagebox as mb
from PIL import ImageTk, Image

# EC = ERROR CODE
EC_BUSNAME = 1
EC_FILEBUFFERSIZE_HIGH = 2
EC_FILEBUFFERSIZE_LOW = 3
EC_FILEBUFFERSIZE_TYPE = 4
EC_BITRESOLUTION_HIGH = 5
EC_BITRESOLUTION_LOW = 6
EC_BITRESOLUTION_TYPE = 7
EC_BAD_LIMIT = 8
EC_BAD_P2P_VAL = 9
EC_CYCLES_TYPE = 10


class RampUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("Generate Ramp Byte Vector")
        self.pack()

        self.initUI()
        
    def initUI(self):
        self.coverImage()
        self.paramInput()
        self.cyclesInput()
        self.rampLimitInput()
        self.shrinkP2P()
        self.generateButton()
    
    def coverImage(self):
        wfImage = Image.open("Ramp.png")
        wfPhoto = ImageTk.PhotoImage(wfImage)
        self.wfLabel = Label(self, image=wfPhoto)
        self.wfLabel.image = wfPhoto
        self.wfLabel.pack(fill=BOTH)
        
        
    def paramInput(self):
        self.paramFrame = LabelFrame(self, text='Parameter Input')

        self.busName = StringVar()
        self.fileBufferSize = StringVar()
        self.bitResolution = StringVar()
        
        
        self.bnFrame = Frame(self.paramFrame)
        bnLabel = Label(self.bnFrame, text = 'Bus Name', pady=4, padx = 4)
        bnLabel.pack(side = LEFT)
        bnEntry = Entry(self.bnFrame, textvariable = self.busName, width=12)
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
    
    def cyclesInput(self):
        self.cyclesFrame = LabelFrame(self, text = 'Cycles Input')
        
        self.cycles = StringVar()
        
        self.cFrame = Frame(self.cyclesFrame)
        cLabel = Label(self.cFrame, text = "Ramp Cycles", pady=4, padx=4)
        cLabel.pack(side=LEFT)
        cEntry = Entry(self.cFrame, textvariable = self.cycles, width = 12)
        cEntry.pack(side = LEFT)
        self.cFrame.pack(anchor = W)
        
        self.cyclesFrame.pack(fill = BOTH)
        self.cycles.set("1")
    
    def rampLimitInput(self):
        self.ampFrame = LabelFrame(self, text='Ramp Limits')

        self.upperLimit = StringVar()
        self.lowerLimit = StringVar()

        self.ulFrame = Frame(self.ampFrame)
        ulLabel = Label(self.ulFrame, text = 'Upper Limit', pady=4, padx=4)
        ulLabel.pack(side = LEFT)
        ulEntry = Entry(self.ulFrame, textvariable = self.upperLimit, width=12)
        ulEntry.pack(side=LEFT)
        self.ulFrame.pack(anchor = W)

        self.llFrame = Frame(self.ampFrame)
        llLabel = Label(self.llFrame, text = 'Lower Limit', pady=4, padx=4)
        llLabel.pack(side=LEFT)
        llEntry = Entry(self.llFrame, textvariable = self.lowerLimit, width=12)
        llEntry.pack(side=LEFT)
        self.llFrame.pack(anchor = W)

        self.ampFrame.pack(fill=BOTH)

        self.upperLimit.set("4095")
        self.lowerLimit.set("0")
    
    def shrinkP2P(self):
        self.p2pFrame = LabelFrame(self, text='Shrink peak2peak val')

        self.shrinkP2PVal = StringVar()

        self.shrinkFrame = Frame(self.p2pFrame)
        p2pLabel = Label(self.shrinkFrame, text = 'Shrink by: ', pady=4, padx=4)
        p2pLabel.pack(side = LEFT)
        p2pEntry = Entry(self.shrinkFrame, textvariable=self.shrinkP2PVal, width=12)
        p2pEntry.pack(side=LEFT)
        self.shrinkFrame.pack(anchor = W)

        self.p2pFrame.pack(fill=BOTH)

        self.shrinkP2PVal.set('0')
        
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
            if _bitRes > 15:
                error.append(EC_BITRESOLUTION_HIGH)
            elif _bitRes < 1:
                error.append(EC_BITRESOLUTION_LOW)
        except:
            error.append(EC_BITRESOLUTION_TYPE)

        try:
            _cycles = int(self.cycles.get())
            if _cycles < 1:
                _cycles = 1
        except:
            error.append(EC_CYCLES_TYPE)

        try:
            _upLim = int(self.upperLimit.get())
            _loLim = int(self.lowerLimit.get())
            if _loLim > _upLim:
                a = _upLim
                _upLim = _loLim
                _loLim = a

            if EC_BITRESOLUTION_HIGH not in error:
                if EC_BITRESOLUTION_LOW not in error:
                    if EC_BITRESOLUTION_TYPE not in error:
                        maxSineVal = 2 ** _bitRes - 1
                        if _upLim > maxSineVal:
                            _upLim = maxSineVal
        except:
            error.append(EC_BAD_LIMIT)

            
        try:
            _shrinkP2PVal = int(self.shrinkP2PVal.get())
            if _shrinkP2PVal == 0:
                _shrinkP2PVal = None
        except:
            error.append(EC_BAD_P2P_VAL)

        if len(error) > 0:
            for i,err in enumerate(error):
                if err == EC_BUSNAME:
                    errorMessage += "({}) Please enter a bus name\n".format(i)
                elif err == EC_FILEBUFFERSIZE_HIGH:
                    errorMessage += "({}) File buffer size must be 512 or less\n".format(i)
                elif err == EC_FILEBUFFERSIZE_LOW:
                    errorMessage += "({}) File buffer size must be 1 or greater\n".format(i)
                elif err == EC_FILEBUFFERSIZE_TYPE:
                    errorMessage += "({}) File buffer size must be an integer\n".format(i)
                elif err == EC_BITRESOLUTION_HIGH:
                    errorMessage += "({}) Bit resolution must be 15 or less\n".format(i)
                elif err == EC_BITRESOLUTION_LOW:
                    errorMessage += "({}) Bit resolution must be 1 or greater".format(i)
                elif err == EC_BITRESOLUTION_TYPE:
                    errorMessage += "({}) Bit resolution must be an integer\n".format(i)
                elif err == EC_BAD_LIMIT:
                    errorMessage += "({}) Problem with limits. Format: FFF\n".format(i)
                elif err == EC_BAD_P2P_VAL:
                    errorMessage += "({}) Problem with peak2peak val. Set to 0 if not using\n".format(i)
                elif err == EC_CYCLES_TYPE:
                    errorMessage += "({}) Please enter an integer for Ramp Cycles\n".format(i)
                else:
                    errorMessage += "Unknown error encountered\n"

            mb.showinfo("Error", errorMessage)
        else:
            _gr = gr(_busName, _fbs, _bitRes, _cycles, _upLim, _loLim, _shrinkP2PVal)
            _gr.run()
