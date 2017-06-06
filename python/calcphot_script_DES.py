#!/usr/bin/env python

# This script calculates the synthetic magnitudes using iraf.calcphot for WD models using DES filters.

# Line 18 should be changed to the path containing the DES filter curves.
# Line 19 should be changed to the path containing the models. 

import sys
import glob
import os
from pyraf import iraf
from shutil import copyfile
from operator import itemgetter

iraf.stsdas()
iraf.hst_calib()
iraf.synphot()

filterDirName='/Users/jacob/SynphotData/Filter_Curves/20150601a'
modelDirName='/Users/jacob/FermilabData/WDModels/TremblayModels/20170515/models/reddened_models'

filterList = ['u','g','r','i','z','y','v']

# move to model location...
os.chdir(modelDirName)

with open('starList.txt') as f:
    stars = f.readlines()

starFileNameList = [x.strip() for x in stars]

# Loop over starFileNameList...
for starFileName in starFileNameList:

    starName=starFileName.split('.fits')[0]
    #ebv = (starFileName.split('ebv_sfd')[1])[:6]

    copyfile(starFileName, 'temp.txt')

    # Loop over CCDs...
    for iccd in range(1,63):
        
        outputString = "mag." + starName + ".ccd" + str(iccd) + ".ugrizyv.fits"
        #print starName, iccd, filter, filterFileName, outputString
            
        if os.path.isfile(outputString):
            oldOutputString = outputString + "~"
            os.rename(outputString, oldOutputString)

        # Loop over filters...
        for filter in filterList:

            filterFileName = '%s/%s_band_20150601a_syn.ccd%d.fits' % (filterDirName, filter, iccd)
            
            try:
                iraf.calcphot(obsmode = filterFileName, spectrum = "temp.txt", output = outputString, form="abmag", append="yes")
            except:
                print "calcphot failed skipping..."
                continue

        # endfor (filter)

    # endfor (iccd)

    os.remove('temp.txt')

# endfor (starFileName)
exit()
