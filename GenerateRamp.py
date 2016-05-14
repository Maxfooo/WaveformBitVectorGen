'''
Created on May 12, 2016

@author: maxr
'''

import math as m
from FileIO import *
busName = 'DAC_Sinusoid'
fileBufferSize = 512 # 512 lines of bit vectors is the maximum resolution
bitResolution = 12 # bits


class GenerateRamp(object):
    
    
    def __init__(self, busName, fileBufferSize, bitResolution, cycles, upLimit=None, loLimit=None, p2pShrink=None):
        self.busName = busName
        self.fileBufferSize = fileBufferSize
        self.bitResolution = bitResolution
        self.cycles = cycles
        self.upLimit = upLimit
        self.loLimit = loLimit
        self.p2pShrink = p2pShrink
        self.fileIO = FileIO()
        
    def run(self):
        self.genFileHeader()
        self.genRamp()
        self.genWaveformFile()

    def genFileHeader(self):
        header = '{},'
        for j in range(self.bitResolution-1, -1, -1):
            if j == self.bitResolution-1:
                header = header + '[{}] MSB,'.format(j)
            elif j == 0:
                header = header + '[{}] LSB'.format(j)
            else:
                header = header + '[{}],'.format(j)
        self.fileHeader = header.format(self.busName)
        
        
    def genRamp(self):
        maxVal = (2**self.bitResolution - 1)
        #stepLength = self.fileBufferSize / self.cycles / maxVal
        stepSize = self.cycles
        self.byteValues = []
        
        if (self.upLimit == None and self.loLimit == None):
            if self.p2pShrink == None:
                for i in range(self.cycles):
                    for j in range(m.floor(self.fileBufferSize/self.cycles)):
                        s = j*stepSize
                        if s > maxVal:
                            s = maxVal
                        b = format((round(s)),'0{}b'.format(self.bitResolution))
                        b = 'b'+ b
                        self.byteValues.append(b)
        
            else:
                topVal = maxVal - self.p2pShrink
                botVal = self.p2pShrink
                for i in range(self.cycles):
                    for j in range(m.floor(self.fileBufferSize/self.cycles) - self.p2pShrink*2):
                        s = j*stepSize + botVal
                        if s > topVal:
                            s = topVal
                        b = format((round(s)),'0{}b'.format(self.bitResolution))
                        b = 'b'+ b
                        self.byteValues.append(b)
        
        else:
            for i in range(self.cycles):
                for j in range(m.floor(self.fileBufferSize/self.cycles) - ((maxVal - self.upLimit) + self.loLimit)):
                    s = j*stepSize + self.loLimit
                    if s > self.upLimit:
                        s = self.upLimit
                    b = format((round(s)),'0{}b'.format(self.bitResolution))
                    b = 'b'+ b
                    self.byteValues.append(b)
        
    
    def genCSVbyte(self, byteString):
        b = byteString.replace('b','')
        j = ''
        for i in b:
            j = j + i + ','
        j = ',' + j.strip(',')
        return j

    def genWaveformFile(self):
        self.fileIO.saveFile(exten='.csv',ftypes=[('comma separated value', '.csv'),('all files', '.*')],
                        ifilen='myfile.csv')
        waveFile = self.fileIO.getSavedFile()
        waveFile.write(self.fileHeader + '\n')
        for i in self.byteValues:
            waveFile.write(i + self.genCSVbyte(i) + '\n')
        waveFile.close()
