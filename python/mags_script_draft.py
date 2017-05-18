#!/usr/bin/env python

import sys
import glob
import os
from pyraf import iraf
from shutil import copyfile
from operator import itemgetter

iraf.stsdas()
iraf.hst_calib()
iraf.synphot()

#move to filter location

os.chdir('/Users/jacob/SynphotData/Filter_Curves/20150601a')

#create a list of CCDs

CCDList = [None]*64
i = 1
while (i < 63):
    
    input = '/Users/jacob/SynphotData/Filter_Curves/20150601a/' + '*ccd' + str(i) + '.fits'
    CCDList[i] = glob.glob(input)

    i = i + 1

#CCDList[63] = glob.glob('*.average.fits')

#print CCDList[1][0]

#move to model location

os.chdir('/Users/jacob/SynphotData/TremblayModels/new_models/First_Set/ASCII_Files')

with open('starList.txt') as f:
    stars = f.readlines()

stars = [x.strip() for x in stars]

starCount = 0
CCDCount = 1
filterCount = 0
    
while (starCount < len(stars)):

    while (CCDCount < 64):
        iraf.unlearn(iraf.calcphot)

        while (filterCount < 8):

            filter = CCDList[CCDCount][filterCount]
            
            print filter
            print stars[starCount]
            
            copyfile(stars[starCount], 'temp.txt')
            starName = stars[starCount]
            outputString = "mag." + starName[:-14] + ".ccd" + str(CCDCount) + ".ginruvyz.fits"
            #outputString = "test.fits"

            iraf.calcphot(obsmode = filter, spectrum = "temp.txt", output = outputString, form="abmag", append="yes")
    
            filterCount = filterCount + 1

        filterCount = 0
        CCDCount = CCDCount + 1
        os.remove('temp.txt')

    CCDCount = 1
    starCount = starCount + 1


exit()
