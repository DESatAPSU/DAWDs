#!/usr/bin/env python

"""
    combineARCSpectra.py

    Example:

    combineARCSpectra.py --help

    combineARCSpectra.py --fileList 'WDC0442-0536.0086b.ms.fits,WDC0442-0536.0087b.ms.fits,WDC0442-0536.0088b.ms.fits' --verbose 2

    """

##################################

def main():

    import argparse
    import time

    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__, \
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--fileList', \
                        help='a comma-separated list of ARC3.5m spectra to combine')
    parser.add_argument('--verbose', help='verbosity level of output to screen (0,1,2,...)', \
                        default=0, type=int)
    args = parser.parse_args()

    if args.verbose > 0: print args

    status = combineARCSpectra(args)
    
    return status


##################################
# combineARCSpectra

def combineARCSpectra(args):

    import sys
    import glob
    import os
    from pyraf import iraf
    from shutil import copyfile
    from operator import itemgetter
    import pandas as pd

    # Setup relavent IRAF tasks...
    iraf.image()
    iraf.imutil()
    iraf.immatch()
    iraf.onedspec()

    # Grab list of file names from argument list
    #  and convert it into a python list...
    #fnameList = 'WDC0442-0536.0086b.ms.fits,WDC0442-0536.0087b.ms.fits,WDC0442-0536.0088b.ms.fits'
    fnameList = args.fileList
    fnameList = fnameList.split(',')

    # Clean up file name list to exclude any excess blank spaces...
    fileNameList = []
    for fname in fnameList:
        fileName = fname.strip()
        fileNameList.append(fileName)

    # Start a new file name list, for the imsliced
    #  files to be imcombined...
    newFileNameList = []

    # Loop through the input file name list...
    for fileName in fileNameList:

        print fileName

        # Create an output file name...
        baseFileName = os.path.splitext(fileName)[0]+'.tmp'
        outputFileName = baseFileName+'.fits'

        # Delete the any temporary files called tempA00?.fits,
        #  and then run imslice on fileName...
        iraf.imdel('tempA00?.fits')
        iraf.imslice(fileName,'tempA',2)

        # Delete the any temporary files called tempB00?.fits,
        #  and then run imslice on tempA001.fits (an output
        #  from the first imslice)...
        iraf.imdel('tempB00?.fits')
        iraf.imslice('tempA001.fits','tempB',2)

        # Rename the output file tempB001.fits from the second
        #  imslice procedure; tempB001.fits contains the 1D
        #  version of the target spectrum. (The other file, 
        #  tempB002.fits, which we ignore, contains the 1D
        #  version of the sky background spectrum.)
        os.rename('tempB001.fits',outputFileName)

        # Append the output file name to the new file name list...
        newFileNameList.append(outputFileName)

        # Clean up unneeded temporary files...
        iraf.imdel('tempA00?.fits')
        iraf.imdel('tempB00?.fits')


    # Print the list of file names that will be fed to imcombine...
    print newFileNameList

    # Here, we convert the python list into an IRAF list...
    inlist = ''
    for newFileName in newFileNameList:
        inlist = inlist+','+newFileName
    inlist = inlist[1:]
    print inlist

    # Run imcombine to create a median-combined spectrum
    #  and its sigma image...
    medianFile = newFileNameList[0].split('.')[0]+'.median.b.ms.fits'
    sigmaFile = 'sigma-'+newFileNameList[0].split('.')[0]+'.median.b.ms.fits'
    iraf.imdel(medianFile)
    iraf.imdel(sigmaFile)
    iraf.imcombine(inlist, medianFile, combine='median', scale='median', sigma=sigmaFile)

    # Create ASCII text file equivalents...
    medianFileTxt = newFileNameList[0].split('.')[0]+'.median.b.ms.txt'
    sigmaFileTxt = 'sigma-'+newFileNameList[0].split('.')[0]+'.median.b.ms.txt'
    iraf.onedspec.wspectext(medianFile, medianFileTxt)
    iraf.onedspec.wspectext(sigmaFile, sigmaFileTxt)
    
    # Combine median and sigma text files...
    df1 = pd.read_csv(medianFileTxt, header=None, names=['wave','flux'], delim_whitespace=True)
    df2 = pd.read_csv(sigmaFileTxt, header=None, names=['wave','flux_err'], delim_whitespace=True)
    df12 = df1.merge(df2, on='wave')
    outputFile = newFileNameList[0].split('.')[0]+'.median.flm'
    df12.to_csv(outputFile,index=False,sep=' ')


    # Run imcombine to create a mean-combined spectrum
    #  and its sigma image...
    meanFile = newFileNameList[0].split('.')[0]+'.mean.b.ms.fits'
    sigmaFile = 'sigma-'+newFileNameList[0].split('.')[0]+'.mean.b.ms.fits'
    iraf.imdel(meanFile)
    iraf.imdel(sigmaFile)
    iraf.imcombine(inlist, meanFile, combine='average', scale='median', sigma=sigmaFile)

    # Create ASCII text file equivalents...
    meanFileTxt = newFileNameList[0].split('.')[0]+'.mean.b.ms.txt'
    sigmaFileTxt = 'sigma-'+newFileNameList[0].split('.')[0]+'.mean.b.ms.txt'
    iraf.onedspec.wspectext(meanFile, meanFileTxt)
    iraf.onedspec.wspectext(sigmaFile, sigmaFileTxt)
    
    # Combine mean and sigma text files...
    df1 = pd.read_csv(meanFileTxt, header=None, names=['wave','flux'], delim_whitespace=True)
    df2 = pd.read_csv(sigmaFileTxt, header=None, names=['wave','flux_err'], delim_whitespace=True)
    df12 = df1.merge(df2, on='wave')
    outputFile = newFileNameList[0].split('.')[0]+'.mean.flm'
    df12.to_csv(outputFile,index=False,sep=' ')


    return 0


##################################

if __name__ == "__main__":
    main()

##################################
