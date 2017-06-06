#!/usr/bin/env python

# This script takes the SDSS synthetic photometry calcphot results (fits files) from the WD models and organizes the data in a CSV file.
# This should be run in a directory contaning subdirectores of the WDs organized by name. For example:
# jacobs-air-2:DirContainingSubDirectories jacob$ ls
# SSSJ0005-0127	 SSSJ0057-4914	SSSJ0206-4159	SSSJ0243p0119	SSSJ0515-3224

# This script is for the 20170515 set, modification is required on lines 17, 


#!/usr/bin/env python

import numpy as np
import pandas as pd
import pyfits
import glob
import os
import glob

dirNameList = glob.glob('SSSJ?????????')
#dirNameList = ['./testcode']


for dirName in dirNameList:

    print dirName
    os.chdir(dirName)
    
    filenameList = sorted(glob.glob('*.fits'))
    starnameList = [(x.split('.ebv')[0])[4:] for x in filenameList]
    #starnameList = [(x.split('_')[0]) for x in starnameListTemp]

    output = [x.split('_') for x in starnameList]
    outputFileString = output[0][0] + ".SDSS_reddened.mags.csv"
        
    allcatdf = pd.DataFrame()
    
    for i in range(len(filenameList)):
        
        filename = filenameList[i]
        starname = starnameList[i]
        
        hdulist = pyfits.open(filename)
        tbdata = hdulist[1].data
        hdulist.close()
        
        fnameList = tbdata['OBSMODE'].tolist()
        abmagList = tbdata['COUNTRATE'].tolist()
        
        #filterList = [(x.split(',')[1]) for fname in fnameList]
        filterList = [ ((os.path.split(fname)[1]).split(',')[1])[:1] for fname in fnameList ]
        #ccdList = [(fname.split('.')[-2]) for fname in fnameList]
        snameList = len(filterList)*[starname]
        #print filterList
        
        try:
            catdf = pd.DataFrame(np.column_stack([filterList,snameList,abmagList]), columns=['BAND', 'STARNAME','ABMAG'])
            catdf.ABMAG = catdf.ABMAG.astype(float)
            allcatdf = pd.concat([allcatdf,catdf])
        except:
            print 'Failed! %s Continuing to next filename...' % (filename)
            continue

    #endfor (i)

#allcatdf.loc[:,'STARNAMECCDNUM'] = allcatdf.loc[:,'STARNAME'] + '_xxx_' + allcatdf.loc[:,'CCDNUM']
    allcatdf.reset_index(drop=True, inplace=True)

    allcatdf2 = allcatdf.pivot_table('ABMAG', index='STARNAME', columns=['BAND'], aggfunc=sum)

    allcatdf2['STARNAME'] = allcatdf2.index.astype(str)
    allcatdf2['STARNAME'] = allcatdf2['STARNAME'].str.split('_xxx_').str.get(0)

#allcatdf2['CCDNUM'] = allcatdf2.index.astype(str)
#allcatdf2['CCDNUM'] = allcatdf2['CCDNUM'].str.split('_xxx_').str.get(1)
    
    cols = ['STARNAME','u', 'g', 'r', 'i', 'z',]
    allcatdf2 = allcatdf2[cols]
    allcatdf2.reset_index(drop=True, inplace=True)
#allcatdf2.rename(columns = {'y':'Y', 'v':'VR'}, inplace=True)

    allcatdf2.to_csv(outputFileString, index=False)

    os.chdir('..')

#endfor (dirName)

exit()
