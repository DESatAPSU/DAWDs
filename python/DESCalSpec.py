# To run (bash):
# python DESCalSpec.py > DESCalSpec.log 2>&1 &
#
# To run (tcsh):
# python DESCalSpec.py >& DESCalSpec.log &
#
# (In both cases, be sure to edit calspecDir
#  and bandsDir below to their locations on
#  your machine.)

# DLT, 2017-06-06
# based in part on scripts by Jack Mueller and Jacob Robertson.

# Initial setup...
import csv
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import glob
import os
import string
from pyraf import iraf
from pyraf.iraf import stsdas,hst_calib,synphot
import shutil

import pyfits

# Be sure to edit these next two lines appropriately...
calspecDir = '/Users/dtucker/IRAF/SynphotData/grp/hst/cdbs/calspec'
bandsDir = '/Users/dtucker/IRAF/DECam/StdBands_Y3A2'

# List of filter bands (in order of increasing average wavelength)...
bandList = ['g', 'r', 'i', 'z', 'Y']

# This file will contain the raw output from calcphot...
rawOutputFile = 'calspec_stdbands_y3a2.raw.fits'

# If rawOutputFile already exists, rename the
#  current rawOutputFile to rawOutputFile~...
if os.path.isfile(rawOutputFile):
    shutil.move(rawOutputFile, rawOutputFile+'~')

# Create a list of all FITS files in the calspec directory...
specFileNameList = glob.glob(calspecDir+'/*.fits')

# Loop over the list of all FITS files in the calspec directory...
for specFileName in specFileNameList:

    # Extract the basename for specFileName...
    baseName = os.path.basename(specFileName)
    
    print baseName, 

    # Capture specFileNames that won't play well with calcphot
    #  by using a try/except block...
    try:
        # Just consider specFileNames that have WMIN (minimum wavelength)
        # and WMAX (maximum wavelength) keywords in their FITS headers...
        hdulist = pyfits.open(specFileName)
        wavemin = hdulist[0].header['WMIN']
        wavemax = hdulist[0].header['WMAX']
        hdulist.close()
    except:        
        print 'FITS table is missing the WMIN and/or WMAX keywords...  skipping...'
        continue

    print wavemin, wavemax

    # Skip those calspec spectra that do not fully 
    #  cover the range of the DES Y3A2 grizY filter
    #  standard bandpass tables...
    if ( (wavemin > 3000.) or (wavemax < 11000.) ):
        print 'Spectrum does not fully cover DES Y3A2 grizY filter standard bandpasses...  Skipping...'
        continue

    for band in bandList:
        print band, 
        bandFileName = bandsDir+'/y3a2_std_passband_'+band+'.fits'
        print bandFileName
        try:
           iraf.calcphot(obsmode=bandFileName,spectrum=specFileName,out=rawOutputFile,form='abmag',append='yes')
        except:
            print 'Synphot command calcphot failed on this spectrum... continuing...'


# Read in rawOutputFile to create a reformatted version in CSV format...
hdulist = pyfits.open(rawOutputFile)
tbdata = hdulist[1].data

# Extact spectrum names as a list...
snameList = tbdata['TARGETID'].tolist()
snameList = [ (os.path.split(sname)[1].strip()) for sname in snameList ]

# Extact filter names as a list...
fnameList = tbdata['OBSMODE'].tolist()
fnameList = [ (os.path.split(fname)[1].strip().split('.fits')[0][-1]) for fname in fnameList ]

# Extact ABmags as a list...
abmagList = tbdata['COUNTRATE'].tolist()

# Form a pandas dataframe from the filter, spectrum, and abmag lists...
catdf = pd.DataFrame(np.column_stack([fnameList,snameList,abmagList]), columns=['BAND','SPECTRUM','ABMAG'])
catdf.head(10)

# Ensure that ABMAG is a float...
catdf.ABMAG = catdf.ABMAG.astype('float')

# Ensure that there are no duplicate rows...
# (probably no longer necessary since shutil.copyfile
#  has been changed to shutil.move elsewhere in this
#  script)...
catdf.drop_duplicates(inplace=True)

# Pivot the pandas dataframe table so that the filter names are now column names
#  (and the ABmags are arranged by filter column name)...
catdf2 = catdf.pivot_table('ABMAG', index='SPECTRUM', columns=['BAND'], aggfunc=sum)

# Now, SPECTRUM is the index; let's also make it a column...
catdf2['SPECTRUM'] = catdf2.index

# Rearrange the columns in this order:  "SPECTRUM, g, r, i, z, Y"
cols = ['SPECTRUM','g','r','i','z','Y']
catdf2 = catdf2[cols]

# Reset the index of the pandas dataframe to a running id number...
catdf2.reset_index(drop=True, inplace=True)

# This file will contain the final, reformated output, in CSV format...
outputFile = 'calspec_stdbands_y3a2.csv'

# If outputFile already exists, rename the
#  current outputFile to outputFile~...
if os.path.isfile(outputFile):
    shutil.move(outputFile, outputFile+'~')

# Output the the pandas dataframe as a CSV file...
catdf2.to_csv(outputFile, index=False)

# Finis!
exit()

