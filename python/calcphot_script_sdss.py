#!/usr/bin/env python

# This script calculated the synthetic magnitudes using iraf.calcphot for WD models using SDSS filters.

# Line 18 should be changed to the path containing the models. 

import sys
import glob
import os
from pyraf import iraf
from shutil import copyfile
from operator import itemgetter

iraf.stsdas()
iraf.hst_calib()
iraf.synphot()

modelDirName='/Users/jacob/FermilabData/WDModels/TremblayModels/20170515/models/reddened_models'

# move to model location...
os.chdir(modelDirName)

with open('starList.txt') as f:
    stars = f.readlines()

starFileNameList = [x.strip() for x in stars]

# Loop over starFileNameList...
for starFileName in starFileNameList:

    starName=starFileName.split('.newformat')[0]

    copyfile(starFileName, 'temp.fits')

    outputString = "mag." + starName + ".ugriz.fits"
    print starName, outputString
            
    #if os.path.isfile(outputString):
    #	oldOutputString = outputString + "~"
    #	os.rename(outputString, oldOutputString)

    try:
        iraf.calcphot(obsmode = "sdss,u", spectrum = "temp.fits", output = outputString, form="abmag", append="yes")
	iraf.calcphot(obsmode = "sdss,g", spectrum = "temp.fits", output = outputString, form="abmag", append="yes")
	iraf.calcphot(obsmode = "sdss,r", spectrum = "temp.fits", output = outputString, form="abmag", append="yes")
	iraf.calcphot(obsmode = "sdss,i", spectrum = "temp.fits", output = outputString, form="abmag", append="yes")
	iraf.calcphot(obsmode = "sdss,z", spectrum = "temp.fits", output = outputString, form="abmag", append="yes")
	print "success!"
    except:
        print "calcphot failed skipping..."
        continue

    os.remove('temp.fits')

exit()
