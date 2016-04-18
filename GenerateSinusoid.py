'''
Created on Jan 26, 2016

@author: Max Ruiz
'''

import math as m
from FileIO import *

class GenerateSinusoid(object):
    '''
    b111001100000,1,1,1,0,0,1,1,0,0,0,0,0
    '''
    def __init__(self, busName, fileBufferSize, bitResolution):
        self.busName = busName
        self.fileBufferSize = fileBufferSize
        self.bitResolution = bitResolution
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
        sizeByte_2 = (2**self.bitResolution)/2
        sinStepSize = (2*m.pi) / self.fileBufferSize
        self.byteValues = []
        for j in range(self.fileBufferSize):
            b = format((round((sizeByte_2)+((sizeByte_2)*m.sin(j*sinStepSize))))-1,'0{}b'.format(self.bitResolution))
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



