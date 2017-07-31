#!/usr/bin/env python

"""
    wdmodel_extract_bestfit_model_from_hdf5.py

    Run within anaconda WDmodel environment.

    Example:

    wdmodel_extract_bestfit_model_from_hdf5.py --help

    wdmodel_extract_bestfit_model_from_hdf5.py --hdf5File SSSJ0409-4942_sum_full_model.hdf5 --outputCSVFile SSSJ0409-4942_sum_bestfit.csv --verbose 2

    """

##################################

def main():

    import argparse
    import time

    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description=__doc__, \
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--hdf5File', \
                        help='name of the WDmodel full_model file')
    parser.add_argument('--outputCSVFile', \
                        help='name of the CSV file to output')
    parser.add_argument('--verbose', help='verbosity level of output to screen (0,1,2,...)', \
                        default=0, type=int)
    args = parser.parse_args()

    if args.verbose > 0: print args

    status = wdmodel_extract_bestfit_model_from_hdf5(args)
    
    return status


##################################
# wdmodel_extract_bestfit_model_from_hdf5

def wdmodel_extract_bestfit_model_from_hdf5(args):

    import sys
    import os
    from shutil import copyfile
    import pandas as pd
    import h5py

    with h5py.File(fn,'r') as fin:
        xyz = fin['model']
        wave = xyz['wave'].value.astype('float64')
        flux = xyz['flux'].value.astype('float64')
        flux_err = xyz['flux_err'].value.astype('float64')

    wave_series = pd.Series(wave)
    flux_series = pd.Series(flux)
    flux_err_series = pd.Series(flux_err)
    df = pd.concat([wave_series,flux_series,flux_err_series], 
                   axis=1, 
                   keys=['wave','flux','flux_err'])

    df.to_csv(outputFile,index=False)


    return 0


##################################

if __name__ == "__main__":
    main()

##################################
