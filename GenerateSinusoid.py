'''
Created on Jan 26, 2016

@author: Max Ruiz
'''

import math as m
from FileIO import *
busName = 'DAC_Sinusoid'
fileBufferSize = 512 # 512 lines of bit vectors is the maximum resolution
bitResolution = 12 # bits

class GenerateSinusoid(object):
    '''
    b111001100000,1,1,1,0,0,1,1,0,0,0,0,0
    '''
    def __init__(self, busName, fileBufferSize, bitResolution, upLimit=None, loLimit=None, p2pShrink=None):
        self.busName = busName
        self.fileBufferSize = fileBufferSize
        self.bitResolution = bitResolution
        self.upLimit = upLimit
        self.loLimit = loLimit
        self.p2pShrink = p2pShrink
        self.fileIO = FileIO()

    def run(self):
        self.genFileHeader()
        self.genSinusoid()
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

    def genSinusoid(self):
        sizeByte_2 = (2**self.bitResolution - 1)/2
        sinStepSize = (2*m.pi) / self.fileBufferSize
        self.byteValues = []

        if (self.upLimit == None and self.loLimit == None):
            if self.p2pShrink == None:
                for j in range(self.fileBufferSize):
                    b = format((round(sizeByte_2+(sizeByte_2*m.sin(j*sinStepSize)))),'0{}b'.format(self.bitResolution))
                    b = 'b'+ b
                    self.byteValues.append(b)
            else:
                sineP2P = (sizeByte_2 - self.p2pShrink)/2
                for j in range(self.fileBufferSize):
                    b = format((round(sizeByte_2+(sineP2P*m.sin(j*sinStepSize)))),'0{}b'.format(self.bitResolution))
                    b = 'b'+ b
                    self.byteValues.append(b)
        else:
            sineUpLimFactor = self.upLimit/2
            sineLoLimFactor = sizeByte_2 - self.loLimit
            for j in range(self.fileBufferSize):
                sineVal = m.sin(j*sinStepSize)
                if sineVal >= 0:
                    b = format((round(sizeByte_2+(sineUpLimFactor*sineVal))),'0{}b'.format(self.bitResolution))
                    b = 'b'+ b
                    self.byteValues.append(b)
                else:
                    b = format((round(sizeByte_2+(sineLoLimFactor*sineVal))),'0{}b'.format(self.bitResolution))
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

