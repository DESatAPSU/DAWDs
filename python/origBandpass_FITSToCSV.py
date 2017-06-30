# Converts STD_BANDPASSES_Y3A1_FGCM_20170630_extend3000.fits to
#          y3a2_std_passband_extend3000_ugrizYatm.csv
# 
# To run (bash):
# python origBandpass_FITSToCSV.py > origBandpass_FITSToCSV.log 2>&1 &
#
# To run (tcsh):
# python origBandpass_FITSToCSV.py >& origBandpass_FITSToCSV.log &
#
# DLT, 2017-06-30
# based in part on scripts by Jack Mueller and Jacob Robertson.

# Initial setup...
import numpy as np
import pandas as pd

import os
import string
import shutil

import pyfits

# Be sure to edit these next two line2 appropriately...
bandsDir = '/Users/dtucker/IRAF/DECam/StdBands_Y3A2_extend3000'
inputFile = bandsDir+'/'+'STD_BANDPASSES_Y3A1_FGCM_20170630_extend3000.fits'

# List of filter bands (plus atm)...
bandList = ['g', 'r', 'i', 'z', 'Y', 'atm']

# Read in inputFile to create a reformatted version in CSV format...
hdulist = pyfits.open(inputFile)
tbdata = hdulist[1].data

# Create lists from each column...
lambdaList = tbdata['LAMBDA'].tolist()
gList = tbdata['g'].tolist()
rList = tbdata['r'].tolist()
iList = tbdata['i'].tolist()
zList = tbdata['z'].tolist()
YList = tbdata['Y'].tolist()
atmList = tbdata['atm'].tolist()

# Create pandas dataframe from the lists...
df = pd.DataFrame(np.column_stack([lambdaList,gList,rList,iList,zList,YList,atmList]),
                  columns=['lambda','g','r','i','z','Y','atm'])

# Output the full table as a CSV file
outputFile = bandsDir+'/'+'STD_BANDPASSES_Y3A1_FGCM_20170630_extend3000.csv'
if os.path.isfile(outputFile):
    shutil.move(outputFile, outputFile+'~')
df.to_csv(outputFile,index=False)

# Output individual bands (+atm)...
for band in bandList:
    outputFile = bandsDir+'/'+'STD_BANDPASSES_Y3A1_FGCM_20170630_extend3000.'+band+'.csv'
    if os.path.isfile(outputFile):
        shutil.move(outputFile, outputFile+'~')
    columnNames = ['lambda',band]
    df.to_csv(outputFile,index=False,columns=columnNames,header=False)


# Finis!
exit()

