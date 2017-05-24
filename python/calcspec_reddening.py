#!/usr/bin/env python

# This script will applying reddening to spectra. Lines 19, 30, 38 require modification depending on the dataset. 

import sys
import os
import glob
import numpy as np
import pandas as pd
from pyraf import iraf
from shutil import copyfile

iraf.stsdas()
iraf.hst_calib()
iraf.synphot()

# Read in extinction table as Pandas df

extinctList = '/Users/jacob/FermilabData/WDModels/TremblayModels/20170515/extinction_20170515.tbl.txt'
extinct_df = pd.read_csv(extinctList,delim_whitespace=True)

# Re-index df to be indexed by star name
extinct_df = extinct_df.set_index(['objname'], drop=True)


with open('starList.txt') as f:
    stars = f.readlines()

starFileList = [x.strip() for x in stars]
starFileListShort = [(x.split('.newformat')[0]) for x in starFileList]
starList = [(x.split('_')[0]) for x in starFileList]

for i in range(0,len(starFileList)):


    inputFile = str(starFileList[i])
    copyfile(inputFile, 'temp.txt')
    outputString =  str(starFileListShort[i]) + ".ebv_sfd_" + str(extinct_df.loc[starList[i]]['E_B_V_SFD']) + ".fits"

    temp = "temp.txt" + "*ebmv(" + str(extinct_df.loc[starList[i]]['E_B_V_SFD']) + ")"

    iraf.calcspec(spectrum = temp, output = outputString, form='flam')
    os.remove('temp.txt')

exit()
