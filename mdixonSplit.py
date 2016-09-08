# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:42:56 2016

@author: lenw
"""

import dicom
import numpy as np
import os

def SplitMDixonInSubSequences(dir):
    #splits a 4-sequence mDixon group into individual examinations
    #by appending a new suffix to the series instance UID in dicom header
    #field (0x20,0x0e)
    os.chdir(dir)
    listOfFiles = [fn for fn in os.listdir('.') if fn.startswith('MR')]
    for fn in listOfFiles :
        this = dicom.read_file(fn)
        mdTag = this[0x08,0x0008].value[3] #gets the mDixon type tag
        oldSeries = this[0x08,0x103e].value #gets the series description
        newSeries = oldSeries + mdTag #sets the new series description
        this[0x08,0x103e].value = newSeries #overrides the series description
        oldSeriesUID = this[0x20,0x000e].value #gets the current Series UID
        if (mdTag == 'F'):
            this[0x20,0x000e].value = oldSeriesUID + '.1'
        if (mdTag == 'IP'):
            this[0x20,0x000e].value = oldSeriesUID + '.2'
        if (mdTag == 'OP'):
            this[0x20,0x000e].value = oldSeriesUID + '.3'
        if (mdTag == 'W'):
            this[0x20,0x000e].value = oldSeriesUID + '.4'
        this.save_as(mdTag+'-'+fn)


SplitMDixonInSubSequences('/Users/lenw/Dropbox/Public/mDixon')







def GetImageHistogram(dims, datatype, filelist, mtag):
    sliceCount = 0
    arrayImage = np.zeros(dims,dtype=datatype)
    for fn in filelist :
        this = dicom.read_file(fn)
        mdTag = this[0x08,0x0008].value[3] #gets the mDixon type tag
        if (mdTag == mtag):
            arrayImage[:, :, int(sliceCount)] = this.pixel_array
            sliceCount = sliceCount + 1
    binEdge = np.amax(arrayImage) + 1
    arrayHisto = np.histogram(arrayImage,bins=np.arange(1,binEdge))
    temp = arrayHisto[0].tolist()
    return(temp)


def SaveHistoToFile(hp, name, listdata):
    fname = hp + name + '.txt'
    outfile = open(fname,'w')
    for i in listdata:
        outfile.write("%d\n" % i)

histoPath = '/Users/lenw/Documents/Clinical_Studies/Vejle_Projects/mr-normal-histograms/'
work = '/Volumes/CODONICS/DICOM/ST000000'

os.chdir(work + '/SE000007')
listOfFiles = [fn for fn in os.listdir('.') if fn.startswith('MR')]
numberOfFiles = len(listOfFiles)
numberOfSlices = int(numberOfFiles / 4)

ref = dicom.read_file(listOfFiles[0]) #examine only the first file
pixelDims = ( int(ref.Rows),int(ref.Columns), numberOfSlices )
pixelSpacing = ( float(ref.PixelSpacing[0]), float(ref.PixelSpacing[1]), float(ref.SliceThickness) )
dataImageType = ref.pixel_array.dtype

histoIP = GetImageHistogram(pixelDims, dataImageType, listOfFiles, 'IP')
SaveHistoToFile(histoPath, 'IP_1', histoIP)

histoW = GetImageHistogram(pixelDims, dataImageType, listOfFiles, 'W')
SaveHistoToFile(histoPath, 'W_1', histoW)

histoOP = GetImageHistogram(pixelDims, dataImageType, listOfFiles, 'OP')
SaveHistoToFile(histoPath, 'OP_1', histoOP)

histoF = GetImageHistogram(pixelDims, dataImageType, listOfFiles, 'F')
SaveHistoToFile(histoPath, 'F_1', histoF)


os.chdir(work + '/SE000003')
listOfFiles = [fn for fn in os.listdir('.') if fn.startswith('MR')]
numberOfFiles = len(listOfFiles)
numberOfSlices = numberOfFiles

ref = dicom.read_file(listOfFiles[0]) #examine only the first file
pixelDims = ( int(ref.Rows),int(ref.Columns), numberOfSlices )
pixelSpacing = ( float(ref.PixelSpacing[0]), float(ref.PixelSpacing[1]), float(ref.SliceThickness) )
dataImageType = ref.pixel_array.dtype

histoT2 = GetImageHistogram(pixelDims, dataImageType, listOfFiles, 'M')
SaveHistoToFile(histoPath, 'TSE_1', histoT2)


d = '/Volumes/CODONICS/DICOM/ST000000/SE000003'
test = dicom.read_file(d+'/MR000000')
test.SeriesDescription

test.SliceThickness
len( [fn for fn in os.listdir(d) if fn.startswith('MR')] )

